from ninja import ModelSchema, Router, Field, Schema
from typing import List

from .models import PlayerInfo


player_router = Router()
        

class PlayerPositionSchema(Schema):
    position_display: str = Field(None, alias="get_position_display")


class PlayerInfoSchema(ModelSchema):
    position: List[PlayerPositionSchema]
    
    class Config:
        model = PlayerInfo
        model_fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "team_name",
            "picture",
            "position",
        ]
