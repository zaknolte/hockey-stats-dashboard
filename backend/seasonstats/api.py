from ninja import ModelSchema, Router, Field, Schema
from ninja.pagination import paginate
from typing import List
from django.shortcuts import get_object_or_404, get_list_or_404

from .models import RegularSeason, PlayoffSeason, PlayerRegularSeason, PlayerPlayoffSeason, GoalieRegularSeason, GoaliePlayoffSeason, TeamRegularSeason, TeamPlayoffSeason
from teamstats.api import TeamSchema

season_router = Router()


class CurrentSeasonSchema(Schema):
    season: int = Field(..., alias="year")


@season_router.get("/current_season", response=CurrentSeasonSchema)
def get_current_season(request):
    return RegularSeason.objects.order_by("-year")[0]


class AllSeasonsSchema(Schema):
    season: list[int]
    
    #resolver to flatten response to a single list
    @staticmethod
    def resolve_season(obj):
         return [i["season__year"] for i in obj]


@season_router.get("/all_seasons", response=AllSeasonsSchema)
def get_all_seasons(request):
    return PlayerRegularSeason.objects.values("season__year").distinct().order_by("-season__year")


class RegularSeasonSchema(ModelSchema):
    class Config:
        model = RegularSeason
        model_fields = "__all__"

        
@season_router.get("/regular/{year}", response=RegularSeasonSchema)
def get_regular_season(request, year: int):
    return get_object_or_404(RegularSeason.objects.get(year=year))


class PlayoffSeasonSchema(ModelSchema):
    class Config:
        model = PlayoffSeason
        model_fields = "__all__"
        
        
@season_router.get("/playoffs/{year}", response=PlayoffSeasonSchema)
def get_post_season(request, year: int):
    return get_object_or_404(PlayoffSeason.objects.get(year=year))


class PlayerSeasonSchema(ModelSchema):
    # player: PlayerSchema
    name: str = Field(..., alias="player.full_name")
    position: list[str]
    team: str = Field(..., alias="team.name")
    year: int  # needed to use resolver
    season: int = Field(..., alias="season.year")
    class Config:
        model = PlayerRegularSeason
        model_fields = "__all__"

    @staticmethod
    def resolve_year(obj):
        # return just the first year of season 
         return int(str(obj.season.year)[:4])
     
    # Player.position is list of dicts
    # Schema will return - position: [position: {...}, position: {...}]
    # Flatten response to just a list of values with resolver - position: [...]
    @staticmethod
    def resolve_position(obj):
        return [i.position for i in obj.player.position.all()]
     

@season_router.get("/skater/all", response=List[PlayerSeasonSchema])
def get_all_skater_seasons(request, season="All Seasons", season_type="Regular Season", team="All Teams"):
    kwargs = {}
    if season != "All Seasons":
        kwargs["season__year"] = season
    if team != "All Teams":
        kwargs["team__name"] = team
    if season_type == "Regular Season":
        return get_list_or_404(PlayerRegularSeason.objects.select_related("team").select_related("season").select_related("player").prefetch_related("player__position").filter(**kwargs))
    else:
        return get_list_or_404(PlayerPlayoffSeason.objects.select_related("team").select_related("season").select_related("player").prefetch_related("player__position").filter(**kwargs))
    

@season_router.get("/skater/{player_id}", response=List[PlayerSeasonSchema])
def get_single_skater_seasons(request, player_id:str, season="All Seasons", season_type="Regular Season", team="All Teams"):
    # player_name = player_name.replace("-", " ").replace("%20", " ").title()
    kwargs = {"player__pk": player_id}
    if season != "All Seasons":
        kwargs["season__year"] = season
    if team != "All Teams":
        kwargs["team__name"] = team
    if season_type == "Regular Season":
        return get_list_or_404(PlayerRegularSeason.objects.select_related("team").select_related("season").select_related("player").prefetch_related("player__position").filter(**kwargs))
    else:
        return get_list_or_404(PlayerPlayoffSeason.objects.select_related("team").select_related("season").select_related("player").prefetch_related("player__position").filter(**kwargs))

        
class GoalieSeasonSchema(ModelSchema):
    name: str = Field(..., alias="player.full_name")
    position: list[str]
    team: str = Field(..., alias="team.name")
    year: int  # needed to use resolver
    season: int = Field(..., alias="season.year")
    class Config:
        model = GoalieRegularSeason
        model_fields = "__all__"

    @staticmethod
    def resolve_year(obj):
        # return just the first year of season 
         return int(str(obj.season.year)[:4])
     
    # Player.position is list of dicts
    # Schema will return - position: [position: {...}, position: {...}]
    # Flatten response to just a list of values with resolver - position: [...]
    @staticmethod
    def resolve_position(obj):
        return [i.position for i in obj.player.position.all()]

        
@season_router.get("/goalie/all", response=List[GoalieSeasonSchema])
def get_all_goalie_seasons(request, season="All Seasons", season_type="Regular Season", team="All Teams"):
    kwargs = {}
    if season != "All Seasons":
        kwargs["season__year"] = season
    if team != "All Teams":
        team = team.replace("-", " ").replace("%20", " ").title()
        kwargs["team__name"] = team
    if season_type == "Regular Season":
        return get_list_or_404(GoalieRegularSeason.objects.select_related("team").select_related("season").select_related("player").prefetch_related("player__position").filter(**kwargs))
    else:
        return get_list_or_404(GoaliePlayoffSeason.objects.select_related("team").select_related("season").select_related("player").prefetch_related("player__position").filter(**kwargs))
    

@season_router.get("/goalie/{player_id}", response=List[GoalieSeasonSchema])
def get_single_goalie_seasons(request, player_id:str, season="All Seasons", season_type="Regular Season", team="All Teams"):
    # player_name = player_name.replace("-", " ").replace("%20", " ").title()
    kwargs = {"player__pk": player_id}
    if season != "All Seasons":
        kwargs["season__year"] = season
    if team != "All Teams":
        team = team.replace("-", " ").replace("%20", " ").title()
        kwargs["team__name"] = team
    if season_type == "Regular Season":
        return get_list_or_404(GoalieRegularSeason.objects.select_related("team").select_related("season").select_related("player").prefetch_related("player__position").filter(**kwargs))
    else:
        return get_list_or_404(GoaliePlayoffSeason.objects.select_related("team").select_related("season").select_related("player").prefetch_related("player__position").filter(**kwargs))
    
    
class TeamSeasonSchema(ModelSchema):
    team: TeamSchema
    year: int
    class Config:
        model = TeamRegularSeason
        model_fields = "__all__"
        
        
    @staticmethod
    def resolve_year(obj):
        # return just the first year of season 
         return int(str(obj.season.year)[:4])
        

@season_router.get("/team/all", response=List[TeamSeasonSchema])
def get_all_team_all_seasons(request):
    return TeamRegularSeason.objects.select_related("team").all()

          
@season_router.get("/team/", response=List[TeamSeasonSchema])
def get_team_seasons(request, team_name="All Teams", season="All Seasons", season_type="Regular Season"):
    kwargs = {}
    
    if team_name != "All Teams":
        # kwargs["team__name"] = team_name
        team = TeamRegularSeason.objects.filter(team__name=team_name)[0]
        kwargs["team__franchise_id"] = team.team.franchise_id
        
    if season != "All Seasons":
        kwargs["season__year"] = season
    if season_type == "Regular Season":
        return get_list_or_404(TeamRegularSeason.objects.select_related("team").select_related("season").filter(**kwargs))
    else:
        return get_list_or_404(TeamPlayoffSeason.objects.select_related("team").select_related("season").filter(**kwargs))


class TeamListSchema(Schema):
    season: int
    season_type: str
    teams: list[str]
    
    @staticmethod
    def resolve_teams(obj):
         names = [i.team.name for i in obj]
         # duplicates if season is 'All Seasons'
         # remove duplicates and re-sort
         return sorted(list(set(names)))
     
    @staticmethod
    def resolve_season(obj):
         return obj[0].season.year
     
    @staticmethod
    def resolve_season_type(obj):
        if obj[0]._meta.model.__name__ == "TeamRegularSeason":
             return "Regular Season"
        elif obj[0]._meta.model.__name__ == "TeamPlayoffSeason":
            return "Playoffs"
        
        return ""


@season_router.get("/team/list/{season}", response=TeamListSchema)
def get_season_team_list(request, season:str, season_type="Regular Season"):
    kwargs = {}
    if season != "All Seasons":
        kwargs["season__year"] = season
    if season_type == "Regular Season":
        return get_list_or_404(TeamRegularSeason.objects.select_related("team").select_related("season").filter(**kwargs).order_by("team__name"))
    elif season_type == "Playoffs":
        return get_list_or_404(TeamPlayoffSeason.objects.select_related("team").select_related("season").filter(**kwargs).order_by("team__name"))
         