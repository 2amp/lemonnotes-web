from django.conf.urls import patterns, url
from lemonnotes import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^start_game/$', views.start_game, name='start_game'),
)
