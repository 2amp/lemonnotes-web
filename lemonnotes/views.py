from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
from lemonnotes import utils
from .models import Realms, Champion, ChampionMatchup
# from .tasks import update_realms, update_champion_list
from time import sleep
# from datetime import datetime
# import pytz
from django.core import serializers

# Create your views here.


def index(request):
    # realms = Realms.get_solo()
    # # This should be done using a celery worker, but I'm poor and can only use 1 heroku dyno.
    # utc = pytz.UTC
    # if (utc.localize(datetime.now()) - realms.last_updated).days > 1:
    #     print 'Updating!'
    #     update_realms()
    #     update_champion_list()
    context_dict = {}
    return render(request, 'lemonnotes/index.html', context_dict)


def build_champion_stats(matches):
    '''Returns a dict of the stats for each champion by champion ID with the following format:
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
                                     'cs': cs,
                                     'image_url': utils.image_url(utils.K_LOL_CHAMP_ICON,
                                                                  Realms.get_solo().n['champion'],
                                                                  Champion.objects.get(idNumber=champion).key),
                                     'name': Champion.objects.get(idNumber=champion).name}
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
    '''Returns an array of stat dicts for the most played champions, sorted by the most played first.'''
    return map(lambda x: dict((x,)), sorted(champion_stats.items(), key=lambda x: x[1]['games'], reverse=True)[:5])


def best_performance_champions_stats(champion_stats, number=5):
    '''Returns an array of stat dicts for the champions on which the summoner has best performed.'''
    for (k, champion_stat) in champion_stats.items():
        champion_stat['wilson'] = utils.wilson_score_interval(champion_stat['wins'], champion_stat['games'] - champion_stat['wins'])
    return map(lambda x: dict((x,)), sorted(champion_stats.items(),
               key=lambda x: utils.wilson_score_interval(x[1]['wins'], x[1]['games'] - x[1]['wins']), reverse=True)[:5])


def get_match_history(region, summoner_id, begin, end):
    '''Gets the match history for a summoner given a begin and end index. This function can only fetch 15 matches at a
    time. Returns an empty array if the bounds are invalid, the request fails, or there are no matches returned.'''
    if begin > end:
        return []
    print 'get_match_history(' + str(begin) + ', ' + str(end) + ')'
    begin_index = 'beginIndex=' + str(begin)
    end_index = 'endIndex=' + str(end)
    url = utils.api_url(utils.K_LOL_MATCH_HISTORY, region, summoner_id, [begin_index, end_index])
    r = requests.get(url, timeout=5)
    matches = []
    if r.status_code == 429:
        # I have no idea how this will affect other threads. Hopefully we can get a greater rate limit so we don't have
        # to resort to doing this.
        sleep(1)
        r = requests.get(url, timeout=5)
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
    '''Returns a dict that describes the solo queue ranked info of the summoner with the given summoner ID with the
    following format: {'tier': tier, 'division': division}. Valid values of tier are 'Unranked', 'Bronze', 'Silver',
    'Gold', 'Platinum', 'Diamond', 'Master', and 'Challenger'. Valid values of division are 'I', 'II', 'III', 'IV', and
    'V' '''
    solo_queue_ranked_info = {'tier': 'Unranked', 'division': ''}
    url = utils.api_url(utils.K_LOL_LEAGUE_SUMMONER_ENTRY, 'na', summoner_id, None)
    print url
    r = requests.get(url, timeout=5)
    if r.status_code == 429:
        # I have no idea how this will affect other threads. Hopefully we can get a greater rate limit so we don't have
        # to resort to doing this.
        sleep(1)
        r = requests.get(url, timeout=5)
    if r.status_code == requests.codes.ok and str(summoner_id) in r.json():
        all_ranked_info = r.json()[str(summoner_id)]
        for queue_info in all_ranked_info:
            if queue_info['queue'] == 'RANKED_SOLO_5x5':
                solo_queue_ranked_info['tier'] = queue_info['tier'].capitalize()
                solo_queue_ranked_info['division'] = queue_info['entries'][0]['division']
    return solo_queue_ranked_info


def summoner_stats(request):
    '''Gets the summoner info dict if the request is a GET and returns an HttpResponse with the most recently played
    matches (currently the last 50 played, but this should be user-specified in the future), a dict returned by
    most_played_champions_stats() that contains stats for the most played champions, and a dict returned by
    solo_queue_ranked_info() that contains the league info for the summoner.'''
    if request.method == 'GET':
        summoner_name = request.GET['summoner_name']
        if len(summoner_name) > 0:
            url = utils.api_url(utils.K_LOL_SUMMONER_BY_NAME, 'na', summoner_name, None)
            r = requests.get(url, timeout=5)
            if r.status_code == 429:
                # I have no idea how this will affect other threads. Hopefully we can get a greater rate limit so we don't have
                # to resort to doing this.
                sleep(1)
                r = requests.get(url, timeout=5)
            if r.status_code == requests.codes.ok:
                summoner_info = r.json().itervalues().next()
                matches = get_matches_for_summoner(summoner_info['id'], int(request.GET['matches_to_fetch']))
                response = r.json().itervalues().next()
                champion_stats = build_champion_stats(matches)
                most_played_champions = most_played_champions_stats(champion_stats)
                solo_queue_ranked_info = get_solo_queue_ranked_info(summoner_info['id'])
                best_performance_champions = best_performance_champions_stats(champion_stats)
                response['mostPlayedChampions'] = most_played_champions
                response['soloQueueRankedInfo'] = solo_queue_ranked_info
                response['bestPerformanceChampions'] = best_performance_champions
                return HttpResponse(json.dumps(response), content_type='application/json; charset=utf-8')
            else:
                print 'API call error! ' + str(r.status_code)
                return HttpResponse({})


def pb_helper(request):
    if request.method == 'POST':
        print '>>> Form POST!'
        print request.POST
        return render(request, 'lemonnotes/pb_helper.html', {'summonerNames': request.POST['summonerNames']})


def champion_list(request):
    return HttpResponse(json.dumps(sorted([champion.name for champion in Champion.objects.all()])), content_type='application/json; charset=utf-8')


def champion_matchup(request):
    champion = request.GET['champion']
    role = request.GET['role']
    if ChampionMatchup.objects.filter(champion=champion, role=role).exists():
        champion_matchup_json = serializers.serialize('json', [ChampionMatchup.objects.get(champion=champion, role=role)])
        champion_matchup = json.loads(champion_matchup_json)[0]['fields']
        champion_matchup = {i: champion_matchup[i] for i in champion_matchup if i not in ['champion', 'role', 'last_updated']}
        for (k, v) in champion_matchup.items():
            champion_matchup[k] = json.loads(v)
        return HttpResponse(json.dumps(champion_matchup), content_type='application/json; charset=utf-8')
    else:
        return HttpResponse()
