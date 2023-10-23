from django.db import models
from teamstats.models import Team


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


class Player(models.Model):
    player_handed_choice = [
        ("Right", "R"),
        ("Left", "L")
    ]
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100)
    team = models.ForeignKey(to=Team, on_delete=models.CASCADE)
    # team_name = models.CharField(max_length=50)
    picture = models.ImageField(upload_to="images", null=True)
    position = models.ManyToManyField(PlayerPosition)
    jersey_number = models.IntegerField()
    birthday = models.DateField()
    birth_city = models.CharField(max_length=50)
    birth_state = models.CharField(max_length=50)
    birth_country = models.CharField(max_length=3)
    height_inches = models.IntegerField()
    weight = models.IntegerField()
    is_active = models.BooleanField()
    is_rookie = models.BooleanField()
    handed = models.CharField(max_length=10, choices=player_handed_choice)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return self.first_name.strip(". ") + " " + self.last_name.strip(". ")

    def save(self, *args, **kwargs):
        self.full_name = self.get_full_name()
        return super().save(*args, **kwargs)
