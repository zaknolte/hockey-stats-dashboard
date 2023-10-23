from ninja import ModelSchema, Router, Field, Schema
from typing import List

from .models import PlayerSeason, Season
from playerstats.api import PlayerInfoSchema

season_router = Router()


class ChampionSchema(Schema):
    name: str
    
    
class SeasonSchema(ModelSchema):
    champion: ChampionSchema
    class Config:
        model = Season
        model_fields = [
            "year",
            "start_date",
            "end_date",
            "season_type",
            "champion"
        ]
        

class PlayerSeasonSchema(ModelSchema):
    player: PlayerInfoSchema
    season: SeasonSchema
    class Config:
        model = PlayerSeason
        model_fields = [
            "id",
            "player",
            "season",
            "goals",
            "assists",
            "points",
        ]


@season_router.get("/players", response=List[PlayerSeasonSchema])
def get_player_season(request, season, season_type="Regular Season", team_name="All Teams"):
    kwargs = {"season__season_type": season_type}
    
    if season != "All Seasons":
        kwargs["season__year"] = season
    if team_name != "All Teams":
        kwargs["player__team_name"] = team_name
        
    return PlayerSeason.objects.filter(**kwargs)

        
class CurrentSeasonSchema(Schema):
    season: int = Field(..., alias="season.year")
        

class SeasonTypeSchema(Schema):
    season_type: str = Field(..., alias="season__season_type")
    

class AllSeasonsSchema(Schema):
    season: int = Field(..., alias="season__year")
        
        
@season_router.get("/current_season", response=CurrentSeasonSchema)
def get_current_season(request):
    return PlayerSeason.objects.order_by("-season__year")[0]


@season_router.get("/all_seasons", response=List[AllSeasonsSchema])
def get_all_seasons(request):
    return PlayerSeason.objects.values("season__year").distinct()
        
        
@season_router.get("/all_season_types", response=List[SeasonTypeSchema])
def get_season_types(request):
    return PlayerSeason.objects.values("season__season_type").distinct()

