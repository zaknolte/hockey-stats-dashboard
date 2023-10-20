from django.db import models

from playerstats.models import PlayerInfo

# Create your models here.
class PlayerSeason(models.Model):
    season_type_choices = [
        ("Pre-Season", "Pre-Season"),
        ("Regular Season", "Regular Season"),
        ("Playoffs", "Playoffs"),
    ]
    player = models.ForeignKey(to=PlayerInfo, on_delete=models.CASCADE)
    season = models.IntegerField()
    season_type = models.CharField(max_length=20, choices=season_type_choices)
    goals = models.IntegerField()
    assists = models.IntegerField()
    points = models.IntegerField()