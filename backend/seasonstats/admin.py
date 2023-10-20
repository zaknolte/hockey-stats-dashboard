from django.contrib import admin
from django.db.models.functions import Lower

from .models import PlayerSeason


# Register your models here.
class PlayerSeasonAdmin(admin.ModelAdmin):
    list_display = ("season", "player", "season_type")
    search_fields = ["season"]

    def get_ordering(self, request):
        return ["season", Lower("player__last_name")]  # sort case insensitive


admin.site.register(PlayerSeason, PlayerSeasonAdmin)