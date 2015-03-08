from lemonnotes_web.keys import RIOT_API_KEY

from math import sqrt

# Taken from LemonNotes/Constants.h

#  riot api urls
BASE_URL = 'https://{server}.api.pvp.net'

# champion
PATH_CHAMPION = 'api/lol/{region}/v1.2/champion'
K_LOL_CHAMPION_LIST = PATH_CHAMPION + ''
K_LOL_CHAMPION = PATH_CHAMPION + '/{path}'

# game
PATH_GAME = 'api/lol/{region}/v1.3/game/by-summoner'
K_LOL_GAME_BY_SUMMONER = PATH_GAME + '/{path}/recent'                       # {summoner_id}

# league
PATH_LEAGUE = 'api/lol/{region}/v2.5/league'
K_LOL_LEAGUE_SUMMONER = PATH_LEAGUE + '/by-summoner/{path}'                 # {summoner_ids}
K_LOL_LEAGUE_SUMMONER_ENTRY = PATH_LEAGUE + '/by-summoner/{path}/entry'     # {summoner_ids}
K_LOL_LEAGUE_TEAM = PATH_LEAGUE + '/by-team/{path}'                         # {summoner_ids}
K_LOL_LEAGUE_TEAM_ENTRY = PATH_LEAGUE + '/by-team/{path}/entry'             # {summoner_ids}
K_LOL_LEAGUE_CHALLENGER = PATH_LEAGUE + '/challenger'                       # {summoner_ids}

# static-data
PATH_STATIC = 'api/lol/static-data/{region}/v1.2'
K_LOL_STATIC_CHAMPION_LIST = PATH_STATIC + '/champion'
K_LOL_STATIC_CHAMPION = PATH_STATIC + '/champion/{path}'                    # {id}
K_LOL_STATIC_ITEM_LIST = PATH_STATIC + '/item'
K_LOL_STATIC_ITEM = PATH_STATIC + '/item/{path}'                            # {id}
K_LOL_STATIC_MASTERY_LIST = PATH_STATIC + '/mastery'
K_LOL_STATIC_MASTERY = PATH_STATIC + '/mastery/{path}'                      # {id}
K_LOL_STATIC_RUNE_LIST = PATH_STATIC + '/rune'
K_LOL_STATIC_RUNE = PATH_STATIC + '/rune/{path}'
K_LOL_STATIC_SPELL_LIST = PATH_STATIC + '/summoner-spell'
K_LOL_STATIC_SPELL = PATH_STATIC + '/summoner-spell/{path}'
K_LOL_STATIC_REALM = PATH_STATIC + "/realm"
K_LOL_STATIC_VERSIONS = PATH_STATIC + "/versions"
K_LOL_STATIC_LANGUAGES = PATH_STATIC + "/languages"
K_LOL_STATIC_LANGUAGE_STRINGS = PATH_STATIC + "/language-strings"

# status
PATH_STATUS = 'shards'
K_LOL_STATUS = PATH_STATUS + ''
K_LOL_STATUS_REGION = PATH_STATUS + '/{path}'                               # {region}

# match
PATH_MATCH = 'api/lol/{region}/v2.2/match'
K_LOL_MATCH = PATH_MATCH + '/{path}'                                        # {match_id}

# match history
PATH_MATCH_HISTORY = 'api/lol/{region}/v2.2/matchhistory'
K_LOL_MATCH_HISTORY = PATH_MATCH_HISTORY + '/{path}'                        # {summoner_id}

# stats
PATH_STATS = 'api/lol/{region}/v1.3/stats/by-summoner'
K_LOL_STATS_RANKED = PATH_STATS + '/{path}/ranked'                          # {summoner_id}
K_LOL_STATS_SUMMARY = PATH_STATS + '/{path}/summary'                        # {summoner_id}

# summoner
PATH_SUMMONER = 'api/lol/{region}/v1.4/summoner'
K_LOL_SUMMONER_BY_NAME = PATH_SUMMONER + '/by-name/{path}'                  # {summoner_name}
K_LOL_SUMMONER = PATH_SUMMONER + '/{path}'                                  # {summoner_id}
K_LOL_SUMMONER_NAMES = PATH_SUMMONER + '/{path}/name'                       # {summoner_id}
K_LOL_SUMMONER_MASTERIES = PATH_SUMMONER + '/{path}/masteries'              # {summoner_id}
K_LOL_SUMMONER_RUNES = PATH_SUMMONER + '/{path}/runes'                      # {summoner_id}

# team
PATH_TEAM = 'api/lol/{region}/v2.4/team'
K_LOL_TEAM_BY_SUMMONER = PATH_TEAM + '/by-summoner/{path}'                  # {summoner_ids}
K_LOL_TEAM = PATH_TEAM + '/{path}'                                          # {team_ids}

# image assets
DDRAGON = "https://ddragon.leagueoflegends.com/cdn"
K_LOL_PROFILE_ICON = DDRAGON + '/{version}/img/profileicon/{key}.png'
K_LOL_CHAMP_SPLASH = DDRAGON + '/img/champion/splash/{key}_0.jpg'
K_LOL_CHAMP_ICON = DDRAGON + '/{version}/img/champion/{key}.png'
K_LOL_SPELL_ICON = DDRAGON + '/{version}/img/spell/{key}.png'
K_LOL_ITEM_ICON = DDRAGON + '/{version}/img/item/{key}.png'


def api_url(call, region, path_param, query_params):
    url = '{0}/{1}?{2}api_key={3}'.format(BASE_URL, call, '{query}', RIOT_API_KEY)
    server = region
    if 'static-data' in url:
        if region == 'euw' or region == 'kr' or region == 'ru' or region == 'tr':
            server = 'global'
        else:
            server = region
    if not path_param:
        path_param = ''
    query_param = ''
    if query_params:
        for param in query_params:
            query_param = query_param + param + '&'
    url = url.format(server=server, region=region, path=path_param, query=query_param)
    return url


def image_url(call, version, key):
    url = call
    if call == K_LOL_CHAMP_SPLASH:
        url = url.format(key=key)
    else:
        url = url.format(version=version, key=key)
    return url


def wilson_score_interval(ups, downs):
    n = ups + downs

    if n == 0:
        return 0

    z = 1.64  # 1.44 = 85%, 1.96 = 95%
    phat = float(ups) / n
    return ((phat + z * z / (2 * n) - z * sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n))
