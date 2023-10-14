from ninja import NinjaAPI
from playerstats.api import player_router, player_season_router

api = NinjaAPI()

api.add_router("/players", player_season_router)
api.add_router("/players/all", player_router)
