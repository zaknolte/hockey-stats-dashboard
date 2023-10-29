from django.db import models

class Team(models.Model):
    conference_choices = [
        ("Western Conference", "Western Conference"),
        ("Eastern Conference", "Eastern Conference"),
    ]
    
    division_choices = [
        ("Pacific Division", "Pacific"),
        ("Central Division", "Central"),
        ("Atlantic Division", "Atlantic"),
        ("Metropolitan Division", "Metropolitan"),
    ]
    
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to="images/team-logo", null=True)
    conference = models.CharField(max_length=50, choices=conference_choices)
    division = models.CharField(max_length=50, choices=division_choices)
    start_season = models.IntegerField()
    final_season = models.IntegerField(default=9999)
    city = models.CharField(max_length=50)
    venue = models.CharField(max_length=50)
    

    def __str__(self):
        return self.name