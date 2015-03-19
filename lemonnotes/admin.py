from django.contrib import admin
from lemonnotes.models import Realms, Champion, ChampionMatchup

# Register your models here.


class ChampionAdmin(admin.ModelAdmin):
    list_display = ('name', 'idNumber')


class ChampionMatchupAdmin(admin.ModelAdmin):
    list_display = ('champion', 'role', 'champions_that_counter', 'champions_that_this_counters')

admin.site.register(Realms)
admin.site.register(Champion, ChampionAdmin)
admin.site.register(ChampionMatchup, ChampionMatchupAdmin)
