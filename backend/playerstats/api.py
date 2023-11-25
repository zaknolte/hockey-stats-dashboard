from ninja import ModelSchema, Router, Field, Schema
from typing import List

from .models import Player
from teamstats.api import TeamSchema


player_router = Router()


class PlayerSchema(ModelSchema):
    # position: List[PlayerPositionSchema]
    position: list[str] = Field(..., alias="position")
    team: TeamSchema
    class Config:
        model = Player
        model_fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "team",
            "picture",
            "position",
            "jersey_number",
            "birthday",
            "birth_city",
            "birth_state",
            "birth_country",
            "height_inches",
            "weight",
            "is_active",
            "is_rookie",
            "handed"
        ]

    # Player.position is list of dicts
    # Schema will return - position: [position: {...}, position: {...}]
    # Flatten response to just a list of values with resolver - position: [...]
    @staticmethod
    def resolve_position(obj):
         return [i.position for i in obj.position.all()]
     
     
class PlayerNameSchema(Schema):
    name: str = Field(..., alias="full_name")
     
     
@player_router.get("/", response=PlayerSchema)
def get_player(request, id):
    return Player.objects.get(pk=id)

@player_router.get("/all", response=List[PlayerSchema])
def get_all_players(request):
    return Player.objects.all()

@player_router.get("/all_names", response=List[PlayerNameSchema])
def get_player_names(request):
    return Player.objects.values("full_name").order_by("full_name")
