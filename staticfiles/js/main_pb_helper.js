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

  // Called when focus leaves search field
  self.onFocusout = function(index, d, e) {
    var championPick = self.championPicks()[index];
    if (!championPick.championName()) {
      championPick.fetchStatus('none');
    }
  };

  self.update = function(index) {
    // ensure that if the pick was selected from the autocomplete dropdown, a change is triggered
    $('.champion-pick').eq(index).change();
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

  self.updateOnKeydown = function(index, d, e) {
    var code = e.keyCode || e.which;
    // 13 is enter, and we don't want the form to submit when enter is pressed. Rather, we want to send a request to
    // the server instead.
    if (code === 13) {
      e.preventDefault();
      self.update(index);
      return false;
    } else if (code === 9) {
      // 9 is tab
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

var mvm = new MatchupViewModel();
ko.applyBindings(mvm);

$(document).ready(function() {
  $.get('/lemonnotes/champion_list/').done(function(data) {
    var champions = [];
    for (var i = 0; i < data.length; i++) {
      champions.push({value: data[i]});
    }
    $('.champion-pick').each(function() {
      $(this).autocomplete({
        lookup: champions,
        onSelect: function (selection) {
          console.log(selection);
        }
      });
    });
  });
});

var dump = function() {
  for (var i = 0; i < NUMBER_OF_SUMMONERS; i++) {
    console.log(mvm.championPicks()[i].championName());
  }
};
