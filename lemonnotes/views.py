from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
from lemonnotes import utils
from lemonnotes.models import Realms, Champion
from time import sleep

# Create your views here.


def index(request):
    context_dict = {}
    return render(request, 'lemonnotes/index.html', context_dict)


def build_champion_stats(matches):
    '''Compiles stats for each summoner by champion ID as a dict with the following format:
    {'1': {'wins': 10, 'games': 20, 'kills': 100, 'deaths': 100, 'assists': 100, 'cs': 100}}'''
    playerStats = {}
    for match in matches:
        info = match['participants'][0]
        champion = info['championId']
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
            playerStats[champion]['image_url'] = utils.image_url(utils.K_LOL_CHAMP_ICON,
                                                                 Realms.get_solo().n['champion'],
                                                                 Champion.objects.get(idNumber=champion).key)
            print playerStats[champion]['image_url']
        else:
            if winner:
                playerStats[champion]['wins'] = playerStats[champion]['wins'] + 1
            playerStats[champion]['games'] = playerStats[champion]['games'] + 1
            playerStats[champion]['kills'] = playerStats[champion]['kills'] + kills
            playerStats[champion]['deaths'] = playerStats[champion]['deaths'] + deaths
            playerStats[champion]['assists'] = playerStats[champion]['assists'] + assists
            playerStats[champion]['cs'] = playerStats[champion]['cs'] + cs
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
    if r.status_code == 429:
        # I have no idea how this will affect other threads. Hopefully we can get a greater rate limit so we don't have
        # to resort to doing this.
        sleep(1)
        r = requests.get(url)
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


def get_solo_queue_ranked_info(summoner_id):
    solo_queue_ranked_info = {'tier': 'Unranked', 'division': ''}
    url = utils.api_url(utils.K_LOL_LEAGUE_SUMMONER_ENTRY, 'na', summoner_id, None)
    print url
    r = requests.get(url)
    if r.status_code == 429:
        # I have no idea how this will affect other threads. Hopefully we can get a greater rate limit so we don't have
        # to resort to doing this.
        sleep(1)
        r = requests.get(url)
    if r.status_code == requests.codes.ok and str(summoner_id) in r.json():
        all_ranked_info = r.json()[str(summoner_id)]
        for queue_info in all_ranked_info:
            if queue_info['queue'] == 'RANKED_SOLO_5x5':
                solo_queue_ranked_info['tier'] = queue_info['tier'].capitalize()
                solo_queue_ranked_info['division'] = queue_info['entries'][0]['division']
    return solo_queue_ranked_info


def find_summoner(request):
    '''Gets the summoner info dict.'''
    if request.method == 'GET':
        summoner_name = request.GET['summoner_name']
        if len(summoner_name) > 0:
            url = utils.api_url(utils.K_LOL_SUMMONER_BY_NAME, 'na', summoner_name, None)
            r = requests.get(url)
            if r.status_code == 429:
                # I have no idea how this will affect other threads. Hopefully we can get a greater rate limit so we don't have
                # to resort to doing this.
                sleep(1)
                r = requests.get(url)
            if r.status_code == requests.codes.ok:
                summoner_info = r.json().itervalues().next()
                matches = get_matches_for_summoner(summoner_info['id'], 50)
                response = r.json().itervalues().next()
                champion_stats = build_champion_stats(matches)
                most_played_champions = most_played_champions_stats(champion_stats)
                solo_queue_ranked_info = get_solo_queue_ranked_info(summoner_info['id'])
                response['championStats'] = champion_stats
                response['mostPlayedChampions'] = most_played_champions
                response['soloQueueRankedInfo'] = solo_queue_ranked_info
                return HttpResponse(json.dumps(response))
            else:
                print 'API call error! ' + str(r.status_code)
                return HttpResponse()
    else:
        print '>>> Form POST!'
        return HttpResponse()
