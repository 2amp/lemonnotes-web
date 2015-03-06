from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
from lemonnotes import utils, tasks
from lemonnotes.models import Realms
from datetime import datetime
import pytz

# Create your views here.


def index(request):
    # I should probably should cache this?  I also have no idea where to put this...
    t = tasks.add.delay(1, 2)
    print t
    realms = Realms.get_solo()
    utc = pytz.UTC
    # Update realms if it has been longer than one day since it was last updated
    if (datetime.now(utc) - realms.last_updated).days > 1:
        print '>>> Updating realms! Time since last update: {0} days'.format((datetime.now(utc) - realms.last_updated).days)
        url = utils.api_url(utils.K_LOL_STATIC_REALM, 'na', '', None)
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            fetched_realms = r.json()
            realms.v = fetched_realms['v']
            realms.dd = fetched_realms['dd']
            realms.cdn = fetched_realms['cdn']
            realms.lg = fetched_realms['lg']
            realms.n = fetched_realms['n']
            realms.profile_icon_max = fetched_realms['profileiconmax']
            realms.l = fetched_realms['l']
            realms.css = fetched_realms['css']
            realms.save()
    context_dict = {}
    return render(request, 'lemonnotes/index.html', context_dict)


def build_champion_stats(matches):
    '''Compiles stats for each summoner by champion ID as a dict with the following format:
    {'1': {'wins': 10, 'games': 20, 'kills': 100, 'deaths': 100, 'assists': 100, 'cs': 100}}'''
    playerStats = {}
    for match in matches:
        info = match['participants'][0]
        champion = str(info['championId'])
        stats = info['stats']

        winner = stats['winner']
        kills = stats['kills']
        deaths = stats['deaths']
        assists = stats['assists']
        cs = stats['minionsKilled']

        if champion not in playerStats:
            playerStats[champion] = {'wins': 1 if winner else 0,
                                     'games': 1,
                                     'kills': kills,
                                     'deaths': deaths,
                                     'assists': assists,
                                     'cs': cs}
        else:
            if winner:
                playerStats[champion]['wins'] = playerStats[champion]['wins'] + 1
            playerStats[champion]['games'] = playerStats[champion]['games'] + 1
            playerStats[champion]['kills'] = playerStats[champion]['kills'] + kills
            playerStats[champion]['deaths'] = playerStats[champion]['deaths'] + deaths
            playerStats[champion]['assists'] = playerStats[champion]['assists'] + assists
            playerStats[champion]['cs'] = playerStats[champion]['cs'] + cs
            playerStats[champion]['image_link'] = utils.image_url(utils.K_LOL_CHAMP_ICON, Realms.get_solo().n['champion'], 'Lucian')
    return playerStats


def most_played_champions_stats(champion_stats, number=5):
    '''Gets the stat dicts for the most played champions.'''
    return map(lambda x: dict((x,)), sorted(champion_stats.items(), key=lambda x: x[1]['games'], reverse=True)[:5])


def get_match_history(region, summoner_id, begin, end):
    '''Gets the match history for a summoner given a begin and end index. This function can only fetch 15 matches at a
    time.'''
    if begin > end:
        return None
    print 'get_match_history(' + str(begin) + ', ' + str(end) + ')'
    begin_index = 'beginIndex=' + str(begin)
    end_index = 'endIndex=' + str(end)
    url = utils.api_url(utils.K_LOL_MATCH_HISTORY, region, summoner_id, [begin_index, end_index])
    r = requests.get(url)
    matches = []
    if r.status_code == requests.codes.ok and 'matches' in r.json():
        matches = r.json()['matches']
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
            url = utils.api_url(utils.K_LOL_SUMMONER_BY_NAME, 'na', summoner_name, None)
            r = requests.get(url)
            if r.status_code == requests.codes.ok:
                summoner_info = r.json().itervalues().next()
                matches = get_matches_for_summoner(summoner_info['id'], 50)
                response = r.json().itervalues().next()
                champion_stats = build_champion_stats(matches)
                most_played_champions = most_played_champions_stats(champion_stats)
                response['championStats'] = champion_stats
                response['mostPlayedChampions'] = most_played_champions
                return HttpResponse(json.dumps(response))
            else:
                print 'API call error! ' + str(r.status_code)
                return HttpResponse()
    else:
        print '>>> Form POST!'
        return HttpResponse()
