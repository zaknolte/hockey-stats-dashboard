from django.contrib import admin
from django.db.models.functions import Lower

# from .models import Season, PlayerSeason, GoalieSeason, TeamSeason
from .models import RegularSeason, PlayoffSeason, PlayerRegularSeason, PlayerPlayoffSeason, GoalieRegularSeason, GoaliePlayoffSeason, TeamRegularSeason, TeamPlayoffSeason


class RegularSeasonAdmin(admin.ModelAdmin):
    list_display = ("year",)
    search_fields = ["year"]

    def get_ordering(self, request):
        return ["year"]


admin.site.register(RegularSeason, RegularSeasonAdmin)


class PlayerRegularSeasonAdmin(admin.ModelAdmin):
    list_display = ("get_season_year", "get_player_name")
    search_fields = ["season__year"]
    list_select_related = ('player', 'season')
    
    @admin.display(ordering='season__year', description='Season Year')
    def get_season_year(self, obj):
        return obj.season.year

    @admin.display(ordering='player__full_name', description='Player Name')
    def get_player_name(self, obj):
        return f"{obj.player.last_name}, {obj.player.first_name}"
    
    def get_ordering(self, request):
        return ["-season__year", Lower("player__last_name")]  # sort case insensitive


admin.site.register(PlayerRegularSeason, PlayerRegularSeasonAdmin)

class GoalieRegularSeasonAdmin(admin.ModelAdmin):
    list_display = ("get_season_year", "get_player_name")
    search_fields = ["season__year"]
    list_select_related = ('player', 'season')
    
    @admin.display(ordering='season__year', description='Season Year')
    def get_season_year(self, obj):
        return obj.season.year

    @admin.display(ordering='player__full_name', description='Player Name')
    def get_player_name(self, obj):
        return f"{obj.player.last_name}, {obj.player.first_name}"

    def get_ordering(self, request):
        return ["-season__year", Lower("player__last_name")]  # sort case insensitive


admin.site.register(GoalieRegularSeason, GoalieRegularSeasonAdmin)


class TeamRegularSeasonAdmin(admin.ModelAdmin):
    list_display = ("get_season_year", "get_team_name")
    search_fields = ["season__year"]
    list_select_related = ('team', 'season')
    
    @admin.display(ordering='season__year', description='Season Year')
    def get_season_year(self, obj):
        return obj.season.year

    @admin.display(ordering='team__name', description='Team')
    def get_team_name(self, obj):
        return obj.team.name

    def get_ordering(self, request):
        return ["-season__year", Lower("team__name")]  # sort case insensitive


admin.site.register(TeamRegularSeason, TeamRegularSeasonAdmin)