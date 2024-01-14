from django.contrib import admin
from django.db.models.functions import Lower

from .models import Player, PlayerPosition


class PlayerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "get_team_name")
    search_fields = ["last_name", "team__name"]
    list_select_related = ('team',)

    def get_ordering(self, request):
        return [Lower("last_name")]  # sort case insensitive
    
    @admin.display(ordering='team__name', description='Team')
    def get_team_name(self, obj):
        try:
            return obj.team.name
        except AttributeError:
            return "N/A"


admin.site.register(Player, PlayerAdmin)


class PlayerPositionsAdmin(admin.ModelAdmin):
    list_display = ("get_position_display", )


admin.site.register(PlayerPosition, PlayerPositionsAdmin)