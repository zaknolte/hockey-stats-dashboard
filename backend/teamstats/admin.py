from django.contrib import admin
from django.db.models.functions import Lower

from .models import Team


class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "conference", "division", "start_season", "final_season", "city", "venue")
    search_fields = ["name"]

    def get_ordering(self, request):
        return [Lower("name")]  # sort case insensitive


admin.site.register(Team, TeamAdmin)