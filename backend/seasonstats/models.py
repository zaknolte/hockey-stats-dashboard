from django.db import models

from playerstats.models import PlayerInfo
from teamstats.models import Team


class Season(models.Model):
    season_type_choices = [
        ("Pre-Season", "Pre-Season"),
        ("Regular Season", "Regular Season"),
        ("Playoffs", "Playoffs"),
    ]
    
    year = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    season_type = models.CharField(max_length=20, choices=season_type_choices)
    champion = models.ForeignKey(to=Team, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.year)

class PlayerSeason(models.Model):
    player = models.ForeignKey(to=PlayerInfo, on_delete=models.CASCADE)
    season = models.ForeignKey(to=Season, on_delete=models.CASCADE)
    goals = models.IntegerField()
    goals_pp = models.IntegerField()
    goals_sh = models.IntegerField()
    assists = models.IntegerField()
    assists_pp = models.IntegerField()
    assists_sh = models.IntegerField()
    time_on_ice_minutes = models.IntegerField()
    time_on_ice_minutes_pp = models.IntegerField()
    time_on_ice_minutes_sh = models.IntegerField()
    time_on_ice_seconds = models.IntegerField()
    time_on_ice_seconds_pp = models.IntegerField()
    time_on_ice_seconds_sh = models.IntegerField()
    shots = models.IntegerField()
    hits = models.IntegerField()
    penalty_minutes = models.IntegerField()
    penalties_taken = models.IntegerField()
    penalty_minutes_served = models.IntegerField()
    faceoffs_taken = models.IntegerField()
    faceoffs_won = models.IntegerField()
    faceoffs_lost = models.IntegerField()
    faceoff_percent = models.IntegerField()
    giveaways = models.IntegerField()
    takeaways = models.IntegerField()
    blocked_shots = models.IntegerField()
    plus_minus = models.IntegerField()
    
    def __str__(self):
            return str(self.season.year)
            # return f"{self.season.year} {self.season.season_type} {self.player.full_name}"

class GoalieSeason(models.Model):
    player = models.ForeignKey(to=PlayerInfo, on_delete=models.CASCADE)
    season = models.ForeignKey(to=Season, on_delete=models.CASCADE)
    goals = models.IntegerField()
    assists = models.IntegerField()
    time_on_ice_minutes = models.IntegerField()
    time_on_ice_seconds = models.IntegerField()
    shots_against = models.IntegerField()
    shots_against_pp = models.IntegerField()
    shots_against_sh = models.IntegerField()
    saves = models.IntegerField()
    saves_pp = models.IntegerField()
    saves_sh = models.IntegerField()
    did_win = models.BooleanField()
    
    
class TeamSeason(models.Model):
    team = models.ForeignKey(to=Team, on_delete=models.CASCADE)
    season = models.ForeignKey(to=Season, on_delete=models.CASCADE)
    games_played = models.IntegerField()
    wins = models.IntegerField()
    losses = models.IntegerField()
    overtime_loss = models.IntegerField()
    points = models.IntegerField()
    goals_per_game = models.IntegerField()
    goals_against_per_game = models.IntegerField()
    goals_pp = models.IntegerField()
    goals_against_pp = models.IntegerField()
    goals_sh = models.IntegerField()
    goals_against_sh = models.IntegerField()
    pp_chances = models.IntegerField()
    penalties = models.IntegerField()
    pp_percent = models.IntegerField()
    pk_percent = models.IntegerField()
    shots = models.IntegerField()
    shots_pp = models.IntegerField()
    shots_sh = models.IntegerField()
    shots_per_game = models.IntegerField()
    shots_against = models.IntegerField()
    shots_against_pp = models.IntegerField()
    shots_against_sh = models.IntegerField()
    shots_against_per_game = models.IntegerField()
    shot_percent = models.IntegerField()
    faceoffs_taken = models.IntegerField()
    faceoffs_won = models.IntegerField()
    faceoffs_lost = models.IntegerField()
    faceoff_percent = models.IntegerField()
    save_percent = models.IntegerField()
    rank = models.IntegerField()
    