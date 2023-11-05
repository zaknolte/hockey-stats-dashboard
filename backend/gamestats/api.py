from ninja import ModelSchema, Router, Field, Schema
from typing import List
from datetime import date, datetime

from .models import Event, Game, PlayerGame, GoalieGame, TeamGame
from playerstats.api import PlayerSchema
from teamstats.api import TeamSchema
from seasonstats.api import SeasonSchema


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


class TeamGameSchema(ModelSchema):
    team: TeamSchema
    game: SimpleGameSchema
    class Config:
        model = TeamGame
        model_fields = [
            "team",
            "game",
            "game_number",
            "goals",
            "goals_pp",
            "goals_sh",
            "goals_against",
            "goals_against_pp",
            "goals_against_sh",
            "shots",
            "shots_against",
            "hits",
            "penalty_minutes",
            "penalties_taken",
            "penalty_seconds_served",
            "faceoffs_taken",
            "faceoffs_won",
            "faceoffs_lost",
            "faceoff_percent",
            "giveaways",
            "takeaways",
            "blocked_shots",
        ]


class GameSchema(ModelSchema):
    players: List[PlayerGameSchema]
    home_team: TeamSchema
    away_team: TeamSchema
    season: SeasonSchema
    events: List[EventSchema]
    class Config:
        model = Game
        model_fields = [
            "id",
            "players",
            "home_team",
            "away_team",
            "season",
            "game_date",
            "game_start_time",
            "events"
        ]

@game_router.get("/all", response=List[GameSchema])
def get_all_games(request):
    return Game.objects.all()


@game_router.get("/", response=List[GameSchema])
def get_games(request, season="All Seasons", season_type="Regular Season", team_name="All Teams"):
    kwargs = {"season__season_type": season_type}
    
    if season != "All Seasons":
        kwargs["season__year"] = season
    if team_name != "All Teams":
        kwargs["home_team__name"] = team_name
        kwargs["away_team__name"] = team_name
        
    return Game.objects.filter(**kwargs)

@game_router.get("/game", response=GameSchema)
def get_game(request, id):
    return Game.objects.get(pk=id)


@game_router.get("/results", response=List[TeamGameSchema])
def get_game_results(request, id):
    return TeamGame.objects.filter(game__id=id)

@game_router.get("results/team", response=List[TeamGameSchema])
def get_game_results_by_team(request, team_name, season="All Seasons", season_type="Regular Season"):
    kwargs = {"team__name": team_name}
    
    if season != "All Seasons":
        kwargs["game__season__year"] = season
    if season_type != "All Seasons":
        kwargs["game__season__season_type"] = season_type
                
    return TeamGame.objects.filter(**kwargs)