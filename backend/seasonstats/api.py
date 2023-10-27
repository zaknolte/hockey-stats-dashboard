from ninja import ModelSchema, Router, Field, Schema
from typing import List

from .models import Season, PlayerSeason, GoalieSeason, TeamSeason
from teamstats.api import TeamSchema
from playerstats.api import PlayerSchema

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
        

class AllPlayerSchema(Schema):
    id: int
    player: PlayerSchema
    season: SeasonSchema
    goals: int
    assists: int
    points: int
    time_on_ice_seconds: int
    games_played: int
    goals_pp: int = None
    goals_sh: int = None
    assists_pp: int = None
    assists_sh: int = None
    time_on_ice_seconds_pp: int = None
    time_on_ice_seconds_sh: int = None
    shots: int = None
    hits: int = None
    penalty_minutes: int = None
    penalties_taken: int = None
    penalty_seconds_served: int = None
    faceoffs_taken: int = None
    faceoffs_won: int = None
    faceoffs_lost: int = None
    faceoff_percent: float = None
    giveaways: int = None
    takeaways: int = None
    blocked_shots: int = None
    plus_minus: int = None
    shots_against:int = None
    shots_against_pp:int = None
    shots_against_sh:int = None
    saves:int = None
    saves_pp:int = None
    saves_sh:int = None
    wins:int = None
    

class PlayerSeasonSchema(ModelSchema):
    player: PlayerSchema
    season: SeasonSchema
    class Config:
        model = PlayerSeason
        model_fields = [
            "id",
            "player",
            "season",
            "goals",
            "goals_pp",
            "goals_sh",
            "assists",
            "assists_pp",
            "assists_sh",
            "points",
            "time_on_ice_seconds",
            "time_on_ice_seconds_pp",
            "time_on_ice_seconds_sh",
            "shots",
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
            "plus_minus"
        ]


class GoalieSeasonSchema(ModelSchema):
    player: PlayerSchema
    season: SeasonSchema
    class Config:
        model = GoalieSeason
        model_fields = [
            "id",
            "player",
            "season",
            "goals",
            "assists",
            "time_on_ice_seconds",
            "shots_against",
            "shots_against_pp",
            "shots_against_sh",
            "saves",
            "saves_pp",
            "saves_sh",
            "games_played",
            "wins",
        ]
        
        
class TeamSeasonSchema(ModelSchema):
    team: TeamSchema
    season: SeasonSchema
    class Config:
        model = TeamSeason
        model_fields = [
            "id",
            "team",
            "season",
            "games_played",
            "wins",
            "losses",
            "overtime_loss",
            "points",
            "goals_per_game",
            "goals_against_per_game",
            "goals_pp",
            "goals_against_pp",
            "goals_sh",
            "goals_against_sh",
            "pp_chances",
            "penalty_minutes",
            "penalties_taken",
            "pp_percent",
            "pk_percent",
            "shots",
            "shots_pp",
            "shots_sh",
            "shots_per_game",
            "shots_against",
            "shots_against_pp",
            "shots_against_sh",
            "shots_against_per_game",
            "shot_percent",
            "faceoffs_taken",
            "faceoffs_won",
            "faceoffs_lost",
            "faceoff_percent",
            "save_percent",
            "rank"
        ]    
        

@season_router.get("/players/all", response=List[AllPlayerSchema])
def get__all_player_season(request, season, season_type="Regular Season", team_name="All Teams"):
    kwargs = {"season__season_type": season_type}
    
    if season != "All Seasons":
        kwargs["season__year"] = season
    if team_name != "All Teams":
        kwargs["player__team__name"] = team_name
        
    return list(PlayerSeason.objects.filter(**kwargs)) + list(GoalieSeason.objects.filter(**kwargs))


@season_router.get("/players/skaters", response=List[PlayerSeasonSchema])
def get_skater_season(request, season, season_type="Regular Season", team_name="All Teams"):
    kwargs = {"season__season_type": season_type}
    
    if season != "All Seasons":
        kwargs["season__year"] = season
    if team_name != "All Teams":
        kwargs["player__team__name"] = team_name
        
    return PlayerSeason.objects.filter(**kwargs)


@season_router.get("/players/goalies", response=List[GoalieSeasonSchema])
def get_goalie_season(request, season, season_type="Regular Season", team_name="All Teams"):
    kwargs = {"season__season_type": season_type}
    
    if season != "All Seasons":
        kwargs["season__year"] = season
    if team_name != "All Teams":
        kwargs["player__team__name"] = team_name
        
    return GoalieSeason.objects.filter(**kwargs)


@season_router.get("/teams", response=List[TeamSeasonSchema])
def get_team_season(request, season, season_type="Regular Season", team_name="All Teams"):
    kwargs = {"season__season_type": season_type}
    
    if season != "All Seasons":
        kwargs["season__year"] = season
    if team_name != "All Teams":
        kwargs["team__name"] = team_name
        
    return TeamSeason.objects.filter(**kwargs)

        
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

