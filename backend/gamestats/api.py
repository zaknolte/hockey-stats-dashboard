from ninja import ModelSchema, Router, Field, Schema
from typing import List

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
     
     
class TeamGameSchema(Schema):
    id: int
    name: str
    conference: str
    division: str


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


class GameSchema(ModelSchema):
    players: List[PlayerGameSchema]
    home_team: TeamGameSchema
    away_team: TeamGameSchema
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