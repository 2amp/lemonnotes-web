var NUMBER_OF_SUMMONERS = 5;

var oldChampionNameValues = new Array(NUMBER_OF_SUMMONERS);

function ChampionPick(summonerName) {
  this.summonerName = ko.observable(summonerName);
  this.championName = ko.observable('');
  this.role = ko.observable('');
  this.fetchStatus = ko.observable('none');
}

function MatchupViewModel() {
  var self = this;
  self.championPicks = ko.observableArray();

  for (var i = 0; i < NUMBER_OF_SUMMONERS; i++) {
    self.championPicks.push(new ChampionPick(summonerNames[i]));
  }

  // Called when enter is pressed in a search field
  self.updateOnEnter = function(index, d, e) {
    var code = e.keyCode || e.which;
    if (code === 13) {
      e.preventDefault();
      var championPick = self.championPicks()[index];
      if (championPick.championName()) {
        if (championPick.championName() !== oldChampionNameValues[index]) {
          oldChampionNameValues[index] = championPick.championName();
          championPick.fetchStatus('fetching');
          self.sendRequest(index);
        }
      } else {
        championPick.championName('');
        oldChampionNameValues[index] = '';
        championPick.fetchStatus('none');
      }
      return false;
    } else {
      // allow other keypresses to go through
      return true;
    }
  };

  // Called when focus leaves search field
  self.updateOnFocusout = function(index, d, e) {
    var championPick = self.championPicks()[index];
    if (championPick.championName()) {
      if (championPick.championName() !== oldChampionNameValues[index]) {
        oldChampionNameValues[index] = championPick.championName();
        championPick.fetchStatus('fetching');
        self.sendRequest(index);
      }
    } else {
      championPick.championName('');
      oldChampionNameValues[index] = '';
      championPick.fetchStatus('none');
    }
  };

  // Sends a GET request to /lemonnotes/start_game/ and places data in the Summoner object corresponding to the
  // search field
  self.sendRequest = function(index) {
    var championPick = self.championPicks()[index];
    console.log('Sending request!');
    $.get('/lemonnotes/champion_matchup/', {'champion': championPick.championName(), 'role': championPick.role()})
      .done(function(data) {
        if (data) {
          console.log(data);
          championPick.fetchStatus('valid');
        } else {
          console.log('error!');
          championPick.fetchStatus('invalid');
        }
      })
      .fail(function() {
        console.log('error!');
        championPick.fetchStatus('invalid');
      });
  };
}

ko.applyBindings(new MatchupViewModel());

$(document).ready(function() {
  $.get('/lemonnotes/champion_list/').done(function(data) {
    var champions = data;
    $('.champion-pick').each(function() {
      $(this).autocomplete({source: champions});
    });
  });
});
