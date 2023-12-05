from django.db import models

class Team(models.Model):
    team_id = models.IntegerField(primary_key=True)
    franchise_id = models.IntegerField(null=True)
    name = models.CharField(max_length=50, null=True)
    logo = models.ImageField(upload_to="images/team-logo", null=True)
    conference = models.CharField(max_length=50, null=True)
    division = models.CharField(max_length=50, null=True)
    start_season = models.IntegerField(null=True)
    final_season = models.IntegerField(null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    venue = models.CharField(max_length=50, null=True)
    

    def __str__(self):
        return self.name