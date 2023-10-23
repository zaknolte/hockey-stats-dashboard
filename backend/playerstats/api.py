from ninja import ModelSchema, Router, Field, Schema
from typing import List

from .models import Player


player_router = Router()
        

class PlayerPositionSchema(Schema):
    position: str = Field(..., alias="get_position_display")


class PlayerSchema(ModelSchema):
    position: List[PlayerPositionSchema]
    
    class Config:
        model = Player
        model_fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "team_name",
            "picture",
            "position",
        ]
