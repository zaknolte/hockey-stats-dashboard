from django.contrib import admin
from django.db.models.functions import Lower
# from .models import Game, PlayerGame, TeamGame, GoalieGame, Event
from .models import RegularGame, PlayoffGame, PlayerRegularGame, PlayerPlayoffGame, TeamRegularGame, TeamPlayoffGame, GoalieRegularGame, GoaliePlayoffGame, Event
class RegularGameAdmin(admin.ModelAdmin):
    list_display = ("game_date", "home_team", "away_team")
    search_fields = ["home_team", "away_team"]
    list_select_related = ('home_team', 'away_team')

    def get_ordering(self, request):
        return ["-game_date"]


admin.site.register(RegularGame, RegularGameAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ("period", "period_time_left_seconds", "event_type", "action", "outcome", "coordinates_x", "coordinates_y")
    search_fields = ["event_type", "action"]

    def get_ordering(self, request):
        return [Lower("event_type")]


admin.site.register(Event, EventAdmin)


class PlayerRegularGameAdmin(admin.ModelAdmin):
    list_display = ("player", "game")
    search_fields = ["player", "game"]

    def get_ordering(self, request):
        return ["game", "player"]


admin.site.register(PlayerRegularGame, PlayerRegularGameAdmin)


class GoalieRegularGameAdmin(admin.ModelAdmin):
    list_display = ("player", "game")
    search_fields = ["player", "game"]

    def get_ordering(self, request):
        return ["game", "player"]


admin.site.register(GoalieRegularGame, GoalieRegularGameAdmin)


class TeamRegularGameAdmin(admin.ModelAdmin):
    list_display = ("get_team_name", "get_game_date")
    search_fields = ["team__name", "game__game_date"]
    list_select_related = ('team', 'game')
    raw_id_fields = ("team", "game")

    @admin.display(ordering='team__name', description='Team')
    def get_team_name(self, obj):
        return obj.team.name
    
    @admin.display(ordering='game__game_date', description='Game')
    def get_game_date(self, obj):
        return obj.game.game_date

    def get_ordering(self, request):
        return ["-game__game_date", Lower("team__name")]  # sort case insensitive


admin.site.register(TeamRegularGame, TeamRegularGameAdmin)