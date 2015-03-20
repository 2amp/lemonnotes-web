var NUMBER_OF_SUMMONERS = 5;

function Matchup(summonerName) {
  this.summonerName = ko.observable(summonerName);
  this.championName = ko.observable('');
}

function MatchupViewModel() {
  var self = this;
  self.matchups = ko.observableArray();

  for (var i = 0; i < NUMBER_OF_SUMMONERS; i++) {
    self.matchups.push(new Matchup(summonerNames[i]));
  }
}

ko.applyBindings(new MatchupViewModel());

$(document).ready(function() {
  $.get('/lemonnotes/champion_list/').done(function(data) {
    var champions = JSON.parse(data);
    $('.champion-pick').each(function() {
      $(this).autocomplete({source: champions});
    });
  });
});
