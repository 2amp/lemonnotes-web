from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit


# Not currently used. Probably ok to remove this.
class SummonerSearchForm(forms.Form):
    summoner_1_name = forms.CharField(max_length=256, label='Summoner 1 name', required=False)
    summoner_2_name = forms.CharField(max_length=256, label='Summoner 2 name', required=False)
    summoner_3_name = forms.CharField(max_length=256, label='Summoner 3 name', required=False)
    summoner_4_name = forms.CharField(max_length=256, label='Summoner 4 name', required=False)

    def __init__(self, *args, **kwargs):
        super(SummonerSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = '/lemonnotes/find_summoner/'
        self.helper.add_input(Submit('submit', 'Submit'))
