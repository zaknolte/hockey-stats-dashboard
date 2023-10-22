from django.db import models

from playerstats.models import PlayerInfo
from teamstats.models import Team


class BaseSeason(models.Model):
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
    season = models.ForeignKey(to=BaseSeason, on_delete=models.CASCADE)
    goals = models.IntegerField()
    assists = models.IntegerField()
    points = models.IntegerField()
    
    def __str__(self):
            return str(self.season.year)
            # return f"{self.season.year} {self.season.season_type} {self.player.full_name}"