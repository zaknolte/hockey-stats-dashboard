from django.contrib import admin
from django.db.models.functions import Lower

from .models import Player, PlayerPosition


class PlayerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "get_team_name")
    search_fields = ["last_name", "team__name"]

    def get_ordering(self, request):
        return [Lower("last_name")]  # sort case insensitive
    
    @admin.display(ordering='team__name', description='Team')
    def get_team_name(self, obj):
        return obj.team.name


admin.site.register(Player, PlayerAdmin)


class PlayerPositionsAdmin(admin.ModelAdmin):
    list_display = ("position", )


admin.site.register(PlayerPosition, PlayerPositionsAdmin)