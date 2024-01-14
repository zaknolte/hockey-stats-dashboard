from ninja import ModelSchema, Router, Field, Schema
from typing import List
from datetime import date, datetime
from django.shortcuts import get_object_or_404, get_list_or_404

# from .models import Event, Game, PlayerGame, GoalieGame, TeamRegularGame
from .models import Event, RegularGame, PlayoffGame, PlayerRegularGame, PlayerPlayoffGame, GoalieRegularGame, GoaliePlayoffGame, TeamRegularGame, TeamPlayoffGame
from playerstats.api import PlayerSchema
from teamstats.api import TeamSchema
from seasonstats.api import RegularSeasonSchema


game_router = Router()
        

class PlayerGameSchema(Schema):
    id: int
    full_name: str
    team_name: str = Field(..., alias="team.name")
    position: list[str] = Field(..., alias="position")
    
    # Player.position is list of dicts
    # Schema will return - position: [position: {...}, position: {...}]
    # Flatten response to just a list of values with resolver - position: [...]
    @staticmethod
    def resolve_position(obj):
         return [i.position for i in obj.position.all()]
     
     
class EventSchema(ModelSchema):
    player: PlayerGameSchema

    class Config:
        model = Event
        model_fields = [
            "id",
            "player",
            "period",
            "period_time_left_seconds",
            "event_type",
            "action",
            "outcome",
            "coordinates_x",
            "coordinates_y"
        ]


class SimpleGameSchema(Schema):
    id: int
    season: int = Field(..., alias="season.year")
    game_date: date
    game_start_time: datetime


class TeamRegularGameSchema(ModelSchema):
    team: str = Field(..., alias="team.name")
    # team: TeamSchema
    game: SimpleGameSchema
    class Config:
        model = TeamRegularGame
        model_fields = "__all__"


class GameSchema(ModelSchema):
    players: List[PlayerGameSchema]
    home_team: TeamSchema
    away_team: TeamSchema
    season: RegularSeasonSchema
    # events: List[EventSchema]
    class Config:
        model = RegularGame
        model_fields = [
            "id",
            "players",
            "home_team",
            "away_team",
            "season",
            "game_date",
            "game_start_time",
            # "events"
        ]


@game_router.get("/", response=List[GameSchema])
def get_games(request, season="All Seasons", team_name="All Teams"):
    kwargs = {}
    
    if season != "All Seasons":
        kwargs["season__year"] = season
    if team_name != "All Teams":
        kwargs["home_team__name"] = team_name
        kwargs["away_team__name"] = team_name
        
    return RegularGame.objects.filter(**kwargs)


@game_router.get("/all", response=List[GameSchema])
def get_all_games(request):
    return RegularGame.objects.all()


@game_router.get("/game", response=GameSchema)
def get_game(request, id):
    return get_object_or_404(RegularGame.objects.get(pk=id))


@game_router.get("/results", response=List[TeamRegularGameSchema])
def get_game_results(request, id):
    return get_list_or_404(TeamRegularGame.objects.filter(game__id=id))


@game_router.get("/results/all", response=List[TeamRegularGameSchema])
def get_all_game_results(request):
    return TeamRegularGame.objects.select_related("team").select_related("game").select_related("game__season").all()


@game_router.get("/results/season", response=List[TeamRegularGameSchema])
def get_game_results_by_season(request, season):
    return get_list_or_404(TeamRegularGame.objects.select_related("team").select_related("game").select_related("game__season").filter(game__season__year=season))


@game_router.get("results/team", response=List[TeamRegularGameSchema])
def get_game_results_by_team(request, team_name, season="All Seasons"):
    kwargs = {"team__name": team_name}
    
    if season != "All Seasons":
        kwargs["game__season__year"] = season
                
    return get_list_or_404(TeamRegularGame.objects.select_related("team").select_related("game").select_related("game__season").filter(**kwargs))