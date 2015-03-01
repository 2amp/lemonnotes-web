from django.conf.urls import patterns, url
from lemonnotes import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^find_summoner/$', views.find_summoner, name='find_summoner'),
)
