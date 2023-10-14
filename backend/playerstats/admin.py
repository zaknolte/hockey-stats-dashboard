from django.contrib import admin
from django.db.models.functions import Lower
from .models import PlayerInfo, PlayerSeason, PlayerPosition


class PlayerInfoAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "team_name")
    search_fields = ["last_name"]

    def get_ordering(self, request):
        return [Lower("last_name")]  # sort case insensitive


admin.site.register(PlayerInfo, PlayerInfoAdmin)


class PlayerSeasonAdmin(admin.ModelAdmin):
    list_display = ("season", "player")
    search_fields = ["season"]

    def get_ordering(self, request):
        return ["season", Lower("player__last_name")]  # sort case insensitive


admin.site.register(PlayerSeason, PlayerSeasonAdmin)


class PlayerPositionsAdmin(admin.ModelAdmin):
    list_display = ("position", )


admin.site.register(PlayerPosition, PlayerPositionsAdmin)