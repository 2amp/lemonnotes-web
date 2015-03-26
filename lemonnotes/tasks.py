from __future__ import absolute_import
from lemonnotes_web.celery import app
from celery.decorators import periodic_task
import datetime
from lemonnotes import utils
from .models import Realms, Champion, ChampionMatchup
import requests
import championgg_scraper
import json

# @periodic_task(run_every=datetime.timedelta(seconds=5))
@periodic_task(run_every=datetime.timedelta(days=1))
def update_realms():
    '''Update realms every day.'''
    realms = Realms.get_solo()
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


# @periodic_task(run_every=datetime.timedelta(seconds=5))
@periodic_task(run_every=datetime.timedelta(days=1))
def update_champion_list():
    '''Update champion list every day.'''
    url = utils.api_url(utils.K_LOL_STATIC_CHAMPION_LIST, 'na', '', ['dataById=true'])
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        fetched_champion_list = r.json()['data']
        for k, champion in fetched_champion_list.items():
            if Champion.objects.filter(idNumber=champion['id']).exists():
                c = Champion.objects.get(idNumber=champion['id'])
                c.title = champion['title']
                c.name = champion['name']
                c.key = champion['key']
                c.save()
            else:
                c = Champion(idNumber=champion['id'], title=champion['title'], name=champion['name'], key=champion['key'])
                c.save()


@app.task
def app_task_update_realms():
    update_realms()


@app.task
def app_task_update_champion_list():
    update_champion_list()


def add_matchups_to_db(filename='championgg.json'):
    with open(filename, 'r') as f:
        matchups = json.load(f)
        for matchup in matchups:
            if ChampionMatchup.objects.filter(champion=matchup['champion'], role=matchup['role']).exists():
                cm = ChampionMatchup.objects.get(champion=matchup['champion'], role=matchup['role'])
                cm.champions_that_counter = matchup['champions_that_counter']
                cm.champions_that_this_counters = matchup['champions_that_this_counters']
                cm.support_adcs_that_counter = matchup.get('support_adcs_that_counter', [])
                cm.support_adcs_that_synergize_poorly = matchup.get('support_adcs_that_synergize_poorly', [])
                cm.support_adcs_that_this_counters = matchup.get('support_adcs_that_this_counters', [])
                cm.support_adcs_that_synergize_well = matchup.get('support_adcs_that_synergize_well', [])
                cm.adc_supports_that_counter = matchup.get('adc_supports_that_counter', [])
                cm.adc_supports_that_synergize_poorly = matchup.get('adc_supports_that_synergize_poorly', [])
                cm.adc_supports_that_this_counters = matchup.get('adc_supports_that_this_counters', [])
                cm.adc_supports_that_synergize_well = matchup.get('adc_supports_that_synergize_well', [])
                cm.save()
            else:
                cm = ChampionMatchup(champion=matchup['champion'],
                                     role=matchup['role'],
                                     champions_that_counter=matchup['champions_that_counter'],
                                     champions_that_this_counters=matchup['champions_that_this_counters'],
                                     support_adcs_that_counter=matchup.get('support_adcs_that_counter', []),
                                     support_adcs_that_synergize_poorly=matchup.get('support_adcs_that_synergize_poorly', []),
                                     support_adcs_that_this_counters=matchup.get('support_adcs_that_this_counters', []),
                                     support_adcs_that_synergize_well=matchup.get('support_adcs_that_synergize_well', []),
                                     adc_supports_that_counter=matchup.get('adc_supports_that_counter', []),
                                     adc_supports_that_synergize_poorly=matchup.get('adc_supports_that_synergize_poorly', []),
                                     adc_supports_that_this_counters=matchup.get('adc_supports_that_this_counters', []),
                                     adc_supports_that_synergize_well=matchup.get('adc_supports_that_synergize_well', []))
                cm.save()


@periodic_task(run_every=datetime.timedelta(days=1))
def run_scraper():
    championgg_scraper.scrape()
    add_matchups_to_db()
