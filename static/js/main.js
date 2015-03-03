// Summoner's Rift only right now
var NUMBER_OF_SUMMONERS = 5;

// Array to keep track of old search field values so we don't fetch if the search field value hasn't changed
var oldSearchFieldValues = new Array(NUMBER_OF_SUMMONERS);

// Bound to search fields
function SearchFieldSummoner() {
  this.name = ko.observable('');
  this.isFetching = ko.observable(false);
}

// Bound to stats table
function Summoner() {
  this.name = ko.observable('');
  this.summonerId = ko.observable(0);
  this.stats = ko.observable();
  this.mostPlayedChampions = ko.observableArray();
  this.isDataFetched = ko.observable(false);
}

function SummonerListViewModel() {
  var self = this;
  self.searchFieldSummoners = ko.observableArray();
  self.summoners = ko.observableArray();

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
      if (searchFieldSummoner.name() && searchFieldSummoner.name() !== oldSearchFieldValues[index])
      {
        oldSearchFieldValues[index] = self.searchFieldSummoners()[index].name();
        searchFieldSummoner.isFetching(true);
        self.sendRequest(index);
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
    if (searchFieldSummoner.name() && searchFieldSummoner.name() !== oldSearchFieldValues[index])
    {
      oldSearchFieldValues[index] = self.searchFieldSummoners()[index].name();
      searchFieldSummoner.isFetching(true);
      self.sendRequest(index);
    }
  };

  // Sends a GET request to /lemonnotes/find_summoner/ and places data in the Summoner object corresponding to the
  // search field
  self.sendRequest = function(index) {
    var searchFieldSummoner = self.searchFieldSummoners()[index];
    var summoner = self.summoners()[index];
    if (searchFieldSummoner.name()) {
      console.log('Sending request!');
      $.get('/lemonnotes/find_summoner/', {summoner_name: searchFieldSummoner.name()})
        .done(function(data) {
          console.log($.parseJSON(data));
          data = $.parseJSON(data);
          summoner.name(data.name);
          summoner.summonerId(data.id);
          summoner.isDataFetched(true);
          summoner.stats(data.stats);
          summoner.mostPlayedChampions(data.mostPlayedChampions);
        })
        .fail(function() {
          console.log('error!');
        })
        .always(function() {
          searchFieldSummoner.isFetching(false);
        });
    } else {
      summoner.name('');
      summoner.summonerId(0);
      summoner.stats(null);
      summoner.mostPlayedChampions(null);
      summoner.isDataFetched(false);
    }
  };
}

ko.applyBindings(new SummonerListViewModel());
