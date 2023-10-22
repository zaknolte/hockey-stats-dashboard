from ninja import NinjaAPI
from playerstats.api import player_router
from seasonstats.api import season_router
from teamstats.api import team_router

api = NinjaAPI()

api.add_router("/players", player_router)
api.add_router("/season", season_router)
api.add_router("/teams", team_router)
