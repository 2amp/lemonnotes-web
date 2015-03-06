from __future__ import absolute_import

from celery import shared_task
from celery.decorators import periodic_task
import datetime

from lemonnotes import utils
from .models import Realms, Champion
import requests


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
