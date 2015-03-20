from django.conf.urls import patterns, url
from lemonnotes import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^summoner_stats/$', views.summoner_stats, name='summoner_stats'),
    url(r'^pb_helper/$', views.pb_helper, name='pb_helper'),
    url(r'^champion_list/$', views.champion_list, name='champion_list'),
)
