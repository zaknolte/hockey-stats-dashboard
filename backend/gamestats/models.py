from django.db import models

from playerstats.models import Player
from teamstats.models import Team
from seasonstats.models import RegularSeason, PlayoffSeason


class Event(models.Model):
    player = models.ForeignKey(to=Player, null=True, on_delete=models.SET_NULL)
    period = models.IntegerField()
    period_time_left_seconds = models.IntegerField()
    event_type = models.CharField(max_length=20)
    action = models.CharField(max_length=50)
    outcome = models.CharField(max_length=20)
    coordinates_x = models.IntegerField()
    coordinates_y = models.IntegerField()    


class BaseGame(models.Model):
    players = models.ManyToManyField(to=Player)
    home_team = models.ForeignKey(to=Team, null=True, on_delete=models.SET_NULL, related_name="%(class)s_home_team")
    away_team = models.ForeignKey(to=Team, null=True, on_delete=models.SET_NULL, related_name="%(class)s_away_team")
    game_date = models.DateField(null=True)
    game_start_time = models.DateTimeField(null=True)
    # events = models.ManyToManyField(to=Event, null=True)
    
    
    def __str__(self):
        return f'{self.game_date} {self.away_team} at {self.home_team}'
    
    class Meta:
        abstract = True
    
    
class RegularGame(BaseGame):
    season = models.ForeignKey(to=RegularSeason, on_delete=models.CASCADE)
    
    
class PlayoffGame(BaseGame):
    season = models.ForeignKey(to=PlayoffSeason, on_delete=models.CASCADE)
    
    
class BasePlayerGame(models.Model):
    player = models.ForeignKey(to=Player, on_delete=models.CASCADE)  
    game_number = models.IntegerField(null=True)
    goals = models.IntegerField(null=True)
    goals_pp = models.IntegerField(null=True)
    goals_sh = models.IntegerField(null=True)
    assists = models.IntegerField(null=True)
    assists_pp = models.IntegerField(null=True)
    assists_sh = models.IntegerField(null=True)
    time_on_ice_minutes = models.IntegerField(null=True)
    time_on_ice_minutes_pp = models.IntegerField(null=True)
    time_on_ice_minutes_sh = models.IntegerField(null=True)
    time_on_ice_seconds = models.IntegerField(null=True)
    time_on_ice_seconds_pp = models.IntegerField(null=True)
    time_on_ice_seconds_sh = models.IntegerField(null=True)
    shots = models.IntegerField(null=True)
    hits = models.IntegerField(null=True)
    penalty_minutes = models.IntegerField(null=True)
    penalties_taken = models.IntegerField(null=True)
    penalty_minutes_served = models.IntegerField(null=True)
    faceoffs_taken = models.IntegerField(null=True)
    faceoffs_won = models.IntegerField(null=True)
    faceoffs_lost = models.IntegerField(null=True)
    faceoff_percent = models.IntegerField(null=True)
    giveaways = models.IntegerField(null=True)
    takeaways = models.IntegerField(null=True)
    blocked_shots = models.IntegerField(null=True)
    plus_minus = models.IntegerField(null=True)
    
    def __str__(self):
        return f'{self.player__full_name} {self.game__game_date}'
    
    class Meta:
        abstract = True


class PlayerRegularGame(BasePlayerGame):
    game = models.ForeignKey(to=RegularGame, on_delete=models.CASCADE)
    
    
class PlayerPlayoffGame(BasePlayerGame):
    game = models.ForeignKey(to=PlayoffGame, on_delete=models.CASCADE)


class BaseGoalieGame(models.Model):
    player = models.ForeignKey(to=Player, on_delete=models.CASCADE)
    goals = models.IntegerField(null=True)
    game_number = models.IntegerField(null=True)
    assists = models.IntegerField(null=True)
    time_on_ice_minutes = models.IntegerField(null=True)
    time_on_ice_seconds = models.IntegerField(null=True)
    shots_against = models.IntegerField(null=True)
    shots_against_pp = models.IntegerField(null=True)
    shots_against_sh = models.IntegerField(null=True)
    saves = models.IntegerField(null=True)
    saves_pp = models.IntegerField(null=True)
    saves_sh = models.IntegerField(null=True)
    did_win = models.BooleanField(null=True)

    def __str__(self):
        return f'{self.player__full_name} {self.game__game_date}'
    
    class Meta:
        abstract = True
    

class GoalieRegularGame(BaseGoalieGame):
    game = models.ForeignKey(to=RegularGame, on_delete=models.CASCADE)
    
    
class GoaliePlayoffGame(BaseGoalieGame):
    game = models.ForeignKey(to=PlayoffGame, on_delete=models.CASCADE)


class BaseTeamGame(models.Model):
    team = models.ForeignKey(to=Team, on_delete=models.CASCADE)
    game_number = models.IntegerField(null=True)
    goals = models.IntegerField(null=True)
    goals_pp = models.IntegerField(null=True)
    goals_sh = models.IntegerField(null=True)
    goals_against = models.IntegerField(null=True)
    goals_against_pp = models.IntegerField(null=True)
    goals_against_sh = models.IntegerField(null=True)
    shots = models.IntegerField(null=True)
    shots_against = models.IntegerField(null=True)
    hits = models.IntegerField(null=True)
    penalty_minutes = models.IntegerField(null=True)
    penalties_taken = models.IntegerField(null=True)
    penalty_seconds_served = models.FloatField(null=True)
    faceoffs_taken = models.IntegerField(null=True)
    faceoffs_won = models.IntegerField(null=True)
    faceoffs_lost = models.IntegerField(null=True)
    faceoff_percent = models.FloatField(null=True)
    giveaways = models.IntegerField(null=True)
    takeaways = models.IntegerField(null=True)
    blocked_shots = models.IntegerField(null=True)
    
    def __str__(self):
        return f'{self.team.name} {self.game.game_date}'
    
    class Meta:
        abstract = True

class TeamRegularGame(BaseTeamGame):
    game = models.ForeignKey(to=RegularGame, on_delete=models.CASCADE)
    

class TeamPlayoffGame(BaseTeamGame):
    game = models.ForeignKey(to=PlayoffGame, on_delete=models.CASCADE)