// Summoner's Rift only right now
var NUMBER_OF_SUMMONERS = 5;

// Array to keep track of old search field values so we don't fetch if the search field value hasn't changed
var oldSearchFieldValues = new Array(NUMBER_OF_SUMMONERS);

// Bound to search fields
function SearchFieldSummoner() {
  this.name = ko.observable('');
  this.fetchStatus = ko.observable('none');
}

// Bound to stats table
function Summoner() {
  this.name = ko.observable('');
  this.summonerId = ko.observable(0);
  this.ranking = ko.observable('');
  this.stats = ko.observable();
  this.mostPlayedChampions = ko.observableArray();
  this.bestPerformanceChampions = ko.observableArray();
  this.isDataFetched = ko.observable(false);
}

function SummonerListViewModel() {
  var self = this;
  self.searchFieldSummoners = ko.observableArray();
  self.summoners = ko.observableArray();

  self.matchesToFetchOptions = ko.observableArray([20, 40, 60, 80, 100]);
  self.matchesToFetch = ko.observable(40);

  for (var i = 0; i < NUMBER_OF_SUMMONERS; i++) {
    self.searchFieldSummoners.push(new SearchFieldSummoner());
    self.summoners.push(new Summoner());
  }

  // Called when focus leaves search field
  self.onFocusout = function(index, d, e) {
    var searchFieldSummoner = self.searchFieldSummoners()[index];
    if (!searchFieldSummoner.name()) {
      searchFieldSummoner.fetchStatus('none');
    }
  };

  self.update = function(index) {
    var searchFieldSummoner = self.searchFieldSummoners()[index];
    var summoner = self.summoners()[index];
    if (searchFieldSummoner.name()) {
      if (searchFieldSummoner.name() !== oldSearchFieldValues[index]) {
        oldSearchFieldValues[index] = searchFieldSummoner.name();
        searchFieldSummoner.fetchStatus('fetching');
        self.sendRequest(index);
      }
    } else {
      summoner.name('');
      summoner.summonerId(0);
      summoner.stats(null);
      summoner.mostPlayedChampions(null);
      summoner.bestPerformanceChampions(null);
      summoner.isDataFetched(false);
      oldSearchFieldValues[index] = '';
      searchFieldSummoner.fetchStatus('none');
    }
  };

  self.updateOnKeydown = function(index, d, e) {
    var code = e.keyCode || e.which;
    if (code === 13) {
      e.preventDefault();
      self.update(index);
      return false;
    } else if (code === 9) {
      self.update(index);
      return true;
    } else {
      // allow other keypresses to go through
      return true;
    }
  };

  // Sends a GET request to /lemonnotes/start_game/ and places data in the Summoner object corresponding to the
  // search field
  self.sendRequest = function(index) {
    var searchFieldSummoner = self.searchFieldSummoners()[index];
    var summoner = self.summoners()[index];
    console.log('Sending request!');
    $.get('/lemonnotes/summoner_stats/', {'summoner_name': searchFieldSummoner.name(), 'matches_to_fetch': self.matchesToFetch()})
      .done(function(data) {
        if (data) {
          console.log(data);
          summoner.name(data.name);
          summoner.summonerId(data.id);
          summoner.isDataFetched(true);
          summoner.stats(data.stats);
          summoner.mostPlayedChampions(data.mostPlayedChampions);
          summoner.bestPerformanceChampions(data.bestPerformanceChampions);
          summoner.ranking(data.soloQueueRankedInfo.tier + ' ' + data.soloQueueRankedInfo.division);
          searchFieldSummoner.fetchStatus('valid');
        } else {
          console.log('error!');
          searchFieldSummoner.fetchStatus('invalid');
        }
      })
      .fail(function() {
        console.log('error!');
        searchFieldSummoner.fetchStatus('invalid');
      });
  };

  self.styleFromUrl = function(url) {
    return 'background-image: url("' + url + '");';
  };
}

ko.applyBindings(new SummonerListViewModel());

$(document).ready(function() {
  $('#summoner-search').submit(function() {
    var summonerArray = [];
    for (var i = 0 ; i < NUMBER_OF_SUMMONERS; i++) {
      summonerArray.push($('.summoner-name')[i].value);
    }
    // add summoner names to POST data

    $('<input>').attr('type', 'hidden').attr('name', 'summonerNames').val(JSON.stringify(summonerArray)).appendTo('#summoner-search');
  });
});
