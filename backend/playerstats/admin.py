from django.contrib import admin
from django.db.models.functions import Lower
from .models import Player


class PlayerAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "team_name")
    search_fields = ["last_name"]

    def get_ordering(self, request):
        return [Lower("last_name")]  # sort case insensitive


admin.site.register(Player, PlayerAdmin)
