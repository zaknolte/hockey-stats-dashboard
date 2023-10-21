from ninja import ModelSchema, Router, Field, Schema
from typing import List

from .models import PlayerInfo
from seasonstats.models import PlayerSeason


player_router = Router()
        

class PlayerPositionSchema(Schema):
    position_display: str = Field(None, alias="get_position_display")


class PlayerInfoSchema(ModelSchema):
    position: List[PlayerPositionSchema]
    
    class Config:
        model = PlayerInfo
        model_fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "team_name",
            "picture",
            "position",
        ]


class PlayerSeasonSchema(ModelSchema):
    player: PlayerInfoSchema
    season: int | str
    class Config:
        model = PlayerSeason
        model_fields = [
            "id",
            "player",
            "season",
            "season_type",
            "goals",
            "assists",
            "points",
        ]
        model_fields_optional = ['season']


@player_router.get("/", response=List[PlayerSeasonSchema])
def get_player_season(request, season, season_type="Regular Season", team_name="All Teams"):
    kwargs = {"season_type": season_type}
    
    if season != "All Seasons":
        kwargs["season"] = season
    if team_name != "All Teams":
        kwargs["player__team_name"] = team_name
        
    return PlayerSeason.objects.filter(**kwargs)


class SeasonListSchema(ModelSchema):
    class Config:
        model = PlayerSeason
        model_fields = [
            "season"
        ]
        # model_fields_optional = ['season']
        
        
@player_router.get("/current_season", response=SeasonListSchema)
def get_current_season(request):
    return PlayerSeason.objects.order_by("-season")[0]


@player_router.get("/all_seasons", response=List[SeasonListSchema])
def get_all_seasons(request):
    return PlayerSeason.objects.values("season").distinct()
        
        
@player_router.get("/all_season_types")
def get_season_types(request):
    return dict(PlayerSeason.season_type_choices)

