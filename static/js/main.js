var NUMBER_OF_SUMMONERS = 5;

function SearchFieldSummoner() {
  this.name = ko.observable('');
}

function Summoner() {
  this.name = ko.observable('');
  this.summonerId = ko.observable(0);
  this.matches = ko.observableArray();
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
      console.log(self.summoners()[i].name());
    }
  };

  self.updateOnEnter = function(index, d, e) {
    var code = e.keyCode || e.which;
    if (code === 13) {
      e.preventDefault();
      self.sendRequest(index);
      return false;
    } else {
      // allow other keypresses to go through
      return true;
    }
  };

  self.updateOnFocusout = function(index, d, e) {
    self.sendRequest(index);
  };

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
          summoner.matches(data.matches);
        })
        .fail(function() {
          console.log('error!');
        });
    } else {
      summoner.name('');
      summoner.summonerId(0);
      summoner.isDataFetched(false);
    }
  };
}

ko.applyBindings(new SummonerListViewModel());
