from ninja import NinjaAPI
from playerstats.api import router as player_router

api = NinjaAPI()

api.add_router("/players", player_router)
