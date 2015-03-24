from __future__ import absolute_import

from lemonnotes_web.celery import app
from celery.decorators import periodic_task
import datetime

from lemonnotes import utils
from .models import Realms, Champion, ChampionMatchup
import requests

import os
import json
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals, project
from championgg.spiders.championgg_spider import ChampionGgSpider
from scrapy.utils.project import get_project_settings
from billiard import Process
from subprocess import call


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
def shared_task_update_realms():
    update_realms()


@app.task
def shared_task_update_champion_list():
    update_champion_list()


class UrlCrawlerScript(Process):
    def __init__(self, spider):
        Process.__init__(self)
        os.chdir('championgg')
        if os.path.exists('championgg.json'):
            os.remove('championgg.json')
        settings = get_project_settings()
        self.crawler = Crawler(settings)

        if not hasattr(project, 'crawler'):
            self.crawler.install()
            self.crawler.configure()
            self.crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
        self.spider = spider

    def run(self):
        self.crawler.crawl(self.spider)
        self.crawler.start()
        reactor.run()


def add_matchups_to_db():
    with open('championgg.json', 'r') as f:
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


# @periodic_task(run_every=datetime.timedelta(days=1))
def run_spider():
    print os.getcwd()
    spider = ChampionGgSpider()
    crawler = UrlCrawlerScript(spider)
    crawler.start()
    crawler.join()
    add_matchups_to_db()
    os.chdir('..')


# ugly hack
@periodic_task(run_every=datetime.timedelta(days=1))
def run_spider2():
    os.chdir('championgg')
    call(['scrapy', 'crawl', 'championgg'])
    os.chdir('..')
