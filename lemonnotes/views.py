from django.shortcuts import render
from django.http import HttpResponse
import requests
from lemonnotes import constants
import json

# Create your views here.


def index(request):
    context_dict = {}
    return render(request, 'lemonnotes/index.html', context_dict)


def get_match_history(region, summoner_id, begin, end):
    '''Gets the match history for a summoner given a begin and end index. This function can only fetch 15 matches at a
    time.'''
    if begin > end:
        return None
    print 'get_match_history(' + str(begin) + ', ' + str(end) + ')'
    begin_index = 'beginIndex=' + str(begin)
    end_index = 'endIndex=' + str(end)
    url = constants.api_url(constants.K_LOL_MATCH_HISTORY, region, summoner_id, [begin_index, end_index])
    print url
    r = requests.get(url)
    print r
    matches = []
    if r.status_code == requests.codes.ok and 'matches' in r.json():
        matches = r.json()['matches']
    # matches.reverse()
    return matches


def get_matches_for_summoner(summoner_id, number_of_matches=15):
    '''Gets the given number of matches for a summoner from his match history.'''
    matches = []
    while number_of_matches > 0:
        fetch_limit = min(number_of_matches, 15)
        count = len(matches)
        fetched_matches = get_match_history('na', summoner_id, count, count + fetch_limit)
        if len(fetched_matches) == 0:
            return matches
        matches = matches + fetched_matches
        number_of_matches = number_of_matches - fetch_limit
    return matches


def find_summoner(request):
    '''Gets the summoner info dict.'''
    if request.method == 'GET':
        summoner_name = request.GET['summoner_name']
        if len(summoner_name) > 0:
            url = constants.api_url(constants.K_LOL_SUMMONER_BY_NAME, 'na', summoner_name, None)
            r = requests.get(url)
            if r.status_code == requests.codes.ok:
                summoner_info = r.json().itervalues().next()
                matches = get_matches_for_summoner(summoner_info['id'], 100)
                response = r.json().itervalues().next()
                response['matches'] = matches
                return HttpResponse(json.dumps(response))
            else:
                print 'API call error! ' + str(r.status_code)
                return HttpResponse()
    else:
        print 'Form POST!'
        return HttpResponse()
