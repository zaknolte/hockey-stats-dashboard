from ninja import ModelSchema, Router, Schema
from typing import List, Union
from django.shortcuts import get_object_or_404, get_list_or_404

from .models import Team


team_router = Router()

class SimpleTeamSchema(Schema):
    name: str
    team_id: int
    franchise_id: int
    conference: str
    division: str
    
class TeamSchema(ModelSchema):    
    class Config:
        model = Team
        model_fields = "__all__"


@team_router.get("/", response=TeamSchema)
def get_team(request, team: Union[int, str]):
    kwargs = {}
    if type(team) is int:
        kwargs["pk"] = team
    elif type(team) is str:
        team = team.replace("-", " ").replace("%20", " ").title()
        kwargs["name"] = team
    return get_object_or_404(Team.objects.get(**kwargs))


@team_router.get("/all_teams", response=List[TeamSchema])
def get_all_teams(request):
    return get_object_or_404(Team.objects.order_by("name"))


@team_router.get("/franchise/{pk}", response=List[TeamSchema])
def get_franchise(request, pk):
    return get_list_or_404(Team.objects.filter(franchise_id=pk))