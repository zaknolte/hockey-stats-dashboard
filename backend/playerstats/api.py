from ninja import ModelSchema, Router, Field, Schema
from typing import List

from .models import Player
from teamstats.api import TeamSchema


player_router = Router()
        

class PlayerPositionSchema(Schema):
    position: str = Field(..., alias="get_position_display")


class PlayerSchema(ModelSchema):
    position: List[PlayerPositionSchema]
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
