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

  self.dump = function() {
    for (var i = 0; i < self.summoners().length; i++) {
      console.log(self.summoners()[i]);
    }
  };

  // Called when enter is pressed in a search field
  self.updateOnEnter = function(index, d, e) {
    var code = e.keyCode || e.which;
    if (code === 13) {
      e.preventDefault();
      var searchFieldSummoner = self.searchFieldSummoners()[index];
      var summoner = self.summoners()[index];
      if (searchFieldSummoner.name()) {
        if (searchFieldSummoner.name() !== oldSearchFieldValues[index]) {
          oldSearchFieldValues[index] = self.searchFieldSummoners()[index].name();
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
      return false;
    } else {
      // allow other keypresses to go through
      return true;
    }
  };

  // Called when focus leaves search field
  self.updateOnFocusout = function(index, d, e) {
    var searchFieldSummoner = self.searchFieldSummoners()[index];
    var summoner = self.summoners()[index];
    if (searchFieldSummoner.name()) {
      if (searchFieldSummoner.name() !== oldSearchFieldValues[index]) {
        oldSearchFieldValues[index] = self.searchFieldSummoners()[index].name();
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

  // Sends a GET request to /lemonnotes/find_summoner/ and places data in the Summoner object corresponding to the
  // search field
  self.sendRequest = function(index) {
    var searchFieldSummoner = self.searchFieldSummoners()[index];
    var summoner = self.summoners()[index];
    console.log('Sending request!');
    $.get('/lemonnotes/find_summoner/', {summoner_name: searchFieldSummoner.name(), matches_to_fetch: self.matchesToFetch()})
      .done(function(data) {
        if (data) {
          console.log($.parseJSON(data));
          data = $.parseJSON(data);
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
