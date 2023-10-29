from ninja import ModelSchema, Router
from typing import List

from .models import Team


team_router = Router()


class TeamSchema(ModelSchema):    
    class Config:
        model = Team
        model_fields = [
            "id",
            "name",
            "logo",
            "conference",
            "division",
            "start_season",
            "final_season",
            "city",
            "state",
            "venue",
        ]


@team_router.get("/all_teams", response=List[TeamSchema])
def get_all_teams(request):
    return Team.objects.order_by("name")


@team_router.get("/team", response=TeamSchema)
def get_team(request, name):
    return Team.objects.filter(name=name)[0]