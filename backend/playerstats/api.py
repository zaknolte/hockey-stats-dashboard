from ninja import ModelSchema, Router
from typing import List
from .models import PlayerInfo, PlayerSeason


player_router = Router()


class PlayerInfoSchema(ModelSchema):
    class Config:
        model = PlayerInfo
        model_fields = [
            "id",
            "first_name",
            "last_name",
            "team_name",
            "picture",
        ]


@player_router.get("/", response=List[PlayerInfoSchema])
def get_players(request):
    return PlayerInfo.objects.all()

player_season_router = Router()


class PlayerSeasonSchema(ModelSchema):
    player: PlayerInfoSchema
    class Config:
        model = PlayerSeason
        model_fields = [
            "id",
            "player",
            "season",
            "season_type",
            "goals",
            "assists",
            "points"
        ]


@player_season_router.get("/", response=List[PlayerSeasonSchema])
def get_player_season(request):
    return PlayerSeason.objects.all().order_by('-season')