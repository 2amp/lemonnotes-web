from django import forms


class SummonerSearchForm(forms.form):
    summoner_name = forms.CharField(max_length=256, help_text='Please enter your the name of the summoner.')
