from django.db import models


class PlayerPosition(models.Model):
    player_position_choices = [
        ("Center", "C"),
        ("Right Wing", "RW"),
        ("Left Wing", "LW"),
        ("Right Defense", "RD"),
        ("Left Defense", "LD"),
        ("Goalie", "G"),
    ]
    position = models.CharField(max_length=20, choices=player_position_choices)

    def __str__(self):
        return self.position


class PlayerInfo(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100)
    team_name = models.CharField(max_length=50)
    picture = models.ImageField(upload_to="images")
    position = models.ManyToManyField(PlayerPosition)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return self.first_name.strip(". ") + " " + self.last_name.strip(". ")

    def save(self, *args, **kwargs):
        self.full_name = self.get_full_name()
        return super().save(*args, **kwargs)


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
