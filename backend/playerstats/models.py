from django.db import models


# Create your models here.
class Player(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    team_name = models.CharField(max_length=50)
    goals = models.IntegerField()
    assists = models.IntegerField()
    points = models.IntegerField()
    picture = models.ImageField(upload_to="images")
