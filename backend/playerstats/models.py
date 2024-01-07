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
    full_name = models.CharField(max_length=100, null=True)
    slug = models.SlugField(max_length=100, null=True)
    team = models.ForeignKey(to=Team, on_delete=models.CASCADE, null=True)
    picture = models.CharField(max_length=200, null=True)
    position = models.ManyToManyField(PlayerPosition)
    jersey_number = models.IntegerField(null=True)
    birthday = models.DateField(null=True)
    birth_city = models.CharField(max_length=50, null=True)
    birth_state = models.CharField(max_length=50, null=True)
    birth_country = models.CharField(max_length=3, null=True)
    height_inches = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    is_active = models.BooleanField(null=True)
    is_rookie = models.BooleanField(null=True)
    handed = models.CharField(max_length=10, choices=player_handed_choice, null=True)

    def __str__(self):
        return self.full_name
        
    def get_full_name(self):
        return self.first_name.strip(". ") + " " + self.last_name.strip(". ")
    
    def create_slug(self):
        from django.utils.text import slugify
        return slugify(self.full_name)
    
    def save(self, *args, **kwargs):
        if self.full_name is None:
            self.full_name = self.get_full_name()
        if self.slug is None:
            self.slug = self.create_slug()
        return super().save(*args, **kwargs)
