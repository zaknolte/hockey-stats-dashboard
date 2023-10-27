from django.contrib import admin
from django.db.models.functions import Lower

from .models import Season, PlayerSeason, GoalieSeason, TeamSeason


class SeasonAdmin(admin.ModelAdmin):
    list_display = ("year", "season_type")
    search_fields = ["year"]

    def get_ordering(self, request):
        return ["year"]


admin.site.register(Season, SeasonAdmin)


class PlayerSeasonAdmin(admin.ModelAdmin):
    list_display = ("get_season_year", "get_player_name", "get_season_type")
    search_fields = ["season__year"]
    
    @admin.display(ordering='season__year', description='Season Year')
    def get_season_year(self, obj):
        return obj.season.year

    @admin.display(ordering='player__full_name', description='Player Name')
    def get_player_name(self, obj):
        return obj.player.full_name
    
    @admin.display(ordering='season__season_type', description='Season Type')
    def get_season_type(self, obj):
        return obj.season.season_type

    def get_ordering(self, request):
        return ["season__year", Lower("player__last_name")]  # sort case insensitive


admin.site.register(PlayerSeason, PlayerSeasonAdmin)

class GoalieSeasonAdmin(admin.ModelAdmin):
    list_display = ("get_season_year", "get_player_name", "get_season_type")
    search_fields = ["season__year"]
    
    @admin.display(ordering='season__year', description='Season Year')
    def get_season_year(self, obj):
        return obj.season.year

    @admin.display(ordering='player__full_name', description='Player Name')
    def get_player_name(self, obj):
        return obj.player.full_name
    
    @admin.display(ordering='season__season_type', description='Season Type')
    def get_season_type(self, obj):
        return obj.season.season_type

    def get_ordering(self, request):
        return ["season__year", Lower("player__last_name")]  # sort case insensitive


admin.site.register(GoalieSeason, GoalieSeasonAdmin)


class TeamSeasonAdmin(admin.ModelAdmin):
    list_display = ("get_season_year", "get_team_name", "get_season_type")
    search_fields = ["season__year"]
    
    @admin.display(ordering='season__year', description='Season Year')
    def get_season_year(self, obj):
        return obj.season.year

    @admin.display(ordering='team__name', description='Team')
    def get_team_name(self, obj):
        return obj.team.name
    
    @admin.display(ordering='season__season_type', description='Season Type')
    def get_season_type(self, obj):
        return obj.season.season_type

    def get_ordering(self, request):
        return ["season__year", Lower("team__name")]  # sort case insensitive


admin.site.register(TeamSeason, TeamSeasonAdmin)