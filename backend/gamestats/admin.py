from django.contrib import admin
from django.db.models.functions import Lower
from .models import Game, PlayerGame, TeamGame, GoalieGame, Event

class GameAdmin(admin.ModelAdmin):
    list_display = ("game_date", "home_team", "away_team")
    search_fields = ["home_team", "away_team"]

    def get_ordering(self, request):
        return ["game_date"]


admin.site.register(Game, GameAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ("period", "period_time_left_seconds", "event_type", "action", "outcome", "coordinates_x", "coordinates_y")
    search_fields = ["event_type", "action"]

    def get_ordering(self, request):
        return [Lower("event_type")]


admin.site.register(Event, EventAdmin)


class PlayerGameAdmin(admin.ModelAdmin):
    list_display = ("player", "game")
    search_fields = ["player", "game"]

    def get_ordering(self, request):
        return ["game", "player"]


admin.site.register(PlayerGame, PlayerGameAdmin)


class GoalieGameAdmin(admin.ModelAdmin):
    list_display = ("player", "game")
    search_fields = ["player", "game"]

    def get_ordering(self, request):
        return ["game", "player"]


admin.site.register(GoalieGame, GoalieGameAdmin)


class TeamGameAdmin(admin.ModelAdmin):
    list_display = ("team", "game")
    search_fields = ["team", "game"]

    def get_ordering(self, request):
        return ["game", "team"]


admin.site.register(TeamGame, TeamGameAdmin)