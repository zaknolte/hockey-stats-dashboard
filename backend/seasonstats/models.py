from django.db import models

from playerstats.models import Player
from teamstats.models import Team


class RegularSeason(models.Model):
    year = models.IntegerField(primary_key=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    games_scheduled = models.IntegerField(null=True)
    total_games_played = models.IntegerField(null=True)
    
    def __str__(self):
        return str(self.year)
    
class PlayoffSeason(models.Model):
    year = models.IntegerField(primary_key=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    total_games_played = models.IntegerField(null=True)
    
    def __str__(self):
        return str(self.year)
    
class BaseSkater(models.Model):
    player = models.ForeignKey(to=Player, on_delete=models.CASCADE)
    team = models.ForeignKey(to=Team, on_delete=models.SET_NULL, null=True)
    goals = models.IntegerField(null=True)
    assists = models.IntegerField(null=True)
    points = models.IntegerField(null=True)
    time_on_ice_seconds = models.IntegerField(null=True)
    games_played = models.IntegerField(null=True)
    goals_pp = models.IntegerField(null=True)
    goals_sh = models.IntegerField(null=True)
    assists_pp = models.IntegerField(null=True)
    assists_sh = models.IntegerField(null=True)
    time_on_ice_seconds_pp = models.IntegerField(null=True)
    time_on_ice_seconds_sh = models.IntegerField(null=True)
    shots = models.IntegerField(null=True)
    hits = models.IntegerField(null=True)
    penalty_minutes = models.IntegerField(null=True)
    penalties_taken = models.IntegerField(null=True)
    penalty_seconds_served = models.IntegerField(null=True)
    faceoffs_taken = models.IntegerField(null=True)
    faceoffs_won = models.IntegerField(null=True)
    faceoffs_lost = models.IntegerField(null=True)
    faceoff_percent = models.FloatField(null=True)
    giveaways = models.IntegerField(null=True)
    takeaways = models.IntegerField(null=True)
    blocked_shots = models.IntegerField(null=True)
    plus_minus = models.IntegerField(null=True)
    
    class Meta:
        abstract = True
        
class PlayerRegularSeason(BaseSkater):
    season = models.ForeignKey(to=RegularSeason, on_delete=models.CASCADE)
 
    def __str__(self):
        return f"{self.player.full_name} {self.season.year} Regular Season"
    
    
class PlayerPlayoffSeason(BaseSkater):
    season = models.ForeignKey(to=PlayoffSeason, on_delete=models.CASCADE)
 
    def __str__(self):
        return f"{self.player.full_name} {self.season.year} Playoffs"

class BaseGoalie(models.Model):
    player = models.ForeignKey(to=Player, on_delete=models.CASCADE)
    team = models.ForeignKey(to=Team, on_delete=models.SET_NULL, null=True)
    goals = models.IntegerField(null=True)
    assists = models.IntegerField(null=True)
    points = models.IntegerField(null=True)
    goals_against = models.IntegerField(null=True)
    goals_against_average = models.FloatField(null=True)
    shutouts = models.IntegerField(null=True)
    time_on_ice_seconds = models.IntegerField(null=True)
    games_played = models.IntegerField(null=True)
    shots_against = models.IntegerField(null=True)
    shots_against_pp = models.IntegerField(null=True)
    shots_against_sh = models.IntegerField(null=True)
    saves = models.IntegerField(null=True)
    saves_pp = models.IntegerField(null=True)
    saves_sh = models.IntegerField(null=True)
    save_percent = models.FloatField(null=True)
    wins = models.IntegerField(null=True)
    losses = models.IntegerField(null=True)
    
    class Meta:
        abstract = True


class GoalieRegularSeason(BaseGoalie):
    season = models.ForeignKey(to=RegularSeason, on_delete=models.CASCADE)
 
    def __str__(self):
        return f"{self.player.full_name} {self.season.year} Regular Season"
    
    
class GoaliePlayoffSeason(BaseGoalie):
    season = models.ForeignKey(to=PlayoffSeason, on_delete=models.CASCADE)
 
    def __str__(self):
        return f"{self.player.full_name} {self.season.year} Playoffs"
    
    
class BaseTeam(models.Model):
    team = models.ForeignKey(to=Team, on_delete=models.CASCADE)
    games_played = models.IntegerField(null=True)
    wins = models.IntegerField(null=True)
    home_wins = models.IntegerField(null=True)
    away_wins = models.IntegerField(null=True)
    ties = models.IntegerField(null=True)
    home_ties = models.IntegerField(null=True)
    away_ties = models.IntegerField(null=True)
    losses = models.IntegerField(null=True)
    home_losses = models.IntegerField(null=True)
    away_losses = models.IntegerField(null=True)
    overtime_losses = models.IntegerField(null=True)
    home_overtime_losses = models.IntegerField(null=True)
    away_overtime_losses = models.IntegerField(null=True)
    points = models.IntegerField(null=True)
    goals = models.IntegerField(null=True)
    goals_per_game = models.FloatField(null=True)
    goals_against = models.IntegerField(null=True)
    goals_against_per_game = models.FloatField(null=True)
    goals_pp = models.IntegerField(null=True)
    goals_against_pp = models.IntegerField(null=True)
    goals_sh = models.IntegerField(null=True)
    goals_against_sh = models.IntegerField(null=True)
    pp_chances = models.IntegerField(null=True)
    penalty_minutes = models.IntegerField(null=True)
    penalties_taken = models.IntegerField(null=True)
    pp_percent = models.FloatField(null=True)
    pk_percent = models.FloatField(null=True)
    shots = models.IntegerField(null=True)
    shots_per_game = models.FloatField(null=True)
    shots_against = models.IntegerField(null=True)
    shots_against_per_game = models.FloatField(null=True)
    shot_percent = models.FloatField(null=True)
    faceoffs_taken = models.IntegerField(null=True)
    faceoffs_won = models.IntegerField(null=True)
    faceoffs_lost = models.IntegerField(null=True)
    faceoff_percent = models.FloatField(null=True)
    save_percent = models.FloatField(null=True)
    
    class Meta:
        abstract = True
    

class TeamRegularSeason(BaseTeam):
    season = models.ForeignKey(to=RegularSeason, on_delete=models.CASCADE)
 
    def __str__(self):
        return f"{self.team.name} {self.season.year} Regular Season"
    
    
class TeamPlayoffSeason(BaseTeam):
    season = models.ForeignKey(to=PlayoffSeason, on_delete=models.CASCADE)
 
    def __str__(self):
        return f"{self.team.name} {self.season.year} Playoffs"