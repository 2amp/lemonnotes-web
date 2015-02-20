from django.shortcuts import render
from lemonnotes.forms.SummonerSearchForm

# Create your views here.


def index(request):
    context_dict = {}
    return render(request, 'lemonnotes/index.html', context_dict)


def find_summoner(request):
    if request.method == 'POST':
        form = SummonerSearchForm
