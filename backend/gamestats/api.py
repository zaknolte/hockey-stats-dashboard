from ninja import ModelSchema, Router, Field, Schema
from typing import List

from .models import Event, Game, PlayerGame, GoalieGame, TeamGame
from playerstats.api import PlayerSchema
from teamstats.api import TeamSchema
from seasonstats.api import SeasonSchema


game_router = Router()
        

class EventSchema(ModelSchema):
    player: PlayerSchema

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
    players: List[PlayerSchema]
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
def get_all_games(request, season):
    kwargs = {}
    if season != "All Seasons":
        kwargs["season__year"] = season
        
    return Game.objects.filter(**kwargs)


@game_router.get("/game", response=List[GameSchema])
def get_games(request, season, season_type="Regular Season", team_name="All Teams"):
    kwargs = {"season__season_type": season_type, "season__year": season}

    if team_name != "All Teams":
        kwargs["home_team__name"] = team_name
        kwargs["away_team__name"] = team_name
        
    return Game.objects.filter(**kwargs)

@game_router.get("/game/id", response=GameSchema)
def get_game_by_id(request, pk):
    return Game.objects.get(pk=pk)