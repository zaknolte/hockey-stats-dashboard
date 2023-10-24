from django.contrib import admin
from django.db.models.functions import Lower

from .models import Player, PlayerPosition


class PlayerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "team_name")
    search_fields = ["last_name", "team_name"]

    def get_ordering(self, request):
        return [Lower("last_name")]  # sort case insensitive


admin.site.register(Player, PlayerAdmin)


class PlayerPositionsAdmin(admin.ModelAdmin):
    list_display = ("position", )


admin.site.register(PlayerPosition, PlayerPositionsAdmin)