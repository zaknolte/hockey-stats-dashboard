from django.db import models

from playerstats.models import Player
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
    
    
class BasePlayer(models.Model):
    player = models.ForeignKey(to=Player, on_delete=models.CASCADE)
    season = models.ForeignKey(to=Season, on_delete=models.CASCADE)
    goals = models.IntegerField()
    assists = models.IntegerField()
    points = models.IntegerField()
    time_on_ice_seconds = models.IntegerField()
    games_played = models.IntegerField()
    
    class Meta:
        abstract = True

    def __str__(self):
            return str(self.player.full_name)
        
class PlayerSeason(BasePlayer):
    goals_pp = models.IntegerField()
    goals_sh = models.IntegerField()
    assists_pp = models.IntegerField()
    assists_sh = models.IntegerField()
    time_on_ice_seconds_pp = models.IntegerField()
    time_on_ice_seconds_sh = models.IntegerField()
    shots = models.IntegerField()
    hits = models.IntegerField()
    penalty_minutes = models.IntegerField()
    penalties_taken = models.IntegerField()
    penalty_seconds_served = models.IntegerField()
    faceoffs_taken = models.IntegerField()
    faceoffs_won = models.IntegerField()
    faceoffs_lost = models.IntegerField()
    faceoff_percent = models.FloatField()
    giveaways = models.IntegerField()
    takeaways = models.IntegerField()
    blocked_shots = models.IntegerField()
    plus_minus = models.IntegerField()
    

class GoalieSeason(BasePlayer):
    shots_against = models.IntegerField()
    shots_against_pp = models.IntegerField()
    shots_against_sh = models.IntegerField()
    saves = models.IntegerField()
    saves_pp = models.IntegerField()
    saves_sh = models.IntegerField()
    wins = models.IntegerField()
    
    
class TeamSeason(models.Model):
    team = models.ForeignKey(to=Team, on_delete=models.CASCADE)
    season = models.ForeignKey(to=Season, on_delete=models.CASCADE)
    games_played = models.IntegerField()
    wins = models.IntegerField()
    losses = models.IntegerField()
    overtime_loss = models.IntegerField()
    points = models.IntegerField()
    goals_per_game = models.FloatField()
    goals_against_per_game = models.FloatField()
    goals_pp = models.IntegerField()
    goals_against_pp = models.IntegerField()
    goals_sh = models.IntegerField()
    goals_against_sh = models.IntegerField()
    pp_chances = models.IntegerField()
    penalty_minutes = models.IntegerField()
    penalties_taken = models.IntegerField()
    pp_percent = models.FloatField()
    pk_percent = models.FloatField()
    shots = models.IntegerField()
    shots_pp = models.IntegerField()
    shots_sh = models.IntegerField()
    shots_per_game = models.FloatField()
    shots_against = models.IntegerField()
    shots_against_pp = models.IntegerField()
    shots_against_sh = models.IntegerField()
    shots_against_per_game = models.FloatField()
    shot_percent = models.FloatField()
    faceoffs_taken = models.IntegerField()
    faceoffs_won = models.IntegerField()
    faceoffs_lost = models.IntegerField()
    faceoff_percent = models.FloatField()
    save_percent = models.FloatField()
    rank = models.IntegerField()
    