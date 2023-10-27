from django.db import models

from playerstats.models import Player
from teamstats.models import Team


class Event(models.Model):
    player = models.ForeignKey(to=Player, on_delete=models.CASCADE)
    period = models.IntegerField()
    period_time_left_seconds = models.IntegerField()
    event_type = models.CharField(max_length=20)
    action = models.CharField(max_length=50)
    outcome = models.CharField(max_length=20)
    coordinates_x = models.IntegerField()
    coordinates_y = models.IntegerField()    

class Game(models.Model):
    players = models.ManyToManyField(to=Player)
    home_team = models.ForeignKey(to=Team, on_delete=models.CASCADE, related_name="home_team")
    away_team = models.ForeignKey(to=Team, on_delete=models.CASCADE, related_name="away_team")
    game_date = models.DateField()
    game_start_time = models.DateTimeField()
    events = models.ManyToManyField(to=Event)
    
    
class PlayerGame(models.Model):
    player = models.ForeignKey(to=Player, on_delete=models.CASCADE)  
    game = models.ForeignKey(to=Game, on_delete=models.CASCADE)
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
    

class GoalieGame(models.Model):
    player = models.ForeignKey(to=Player, on_delete=models.CASCADE)
    game = models.ForeignKey(to=Game, on_delete=models.CASCADE)
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
    
    
class TeamGame(models.Model):
    team = models.ForeignKey(to=Team, on_delete=models.CASCADE)
    game = models.ForeignKey(to=Game, on_delete=models.CASCADE)
    goals = models.IntegerField()
    goals_pp = models.IntegerField()
    goals_sh = models.IntegerField()
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