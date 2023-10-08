from ninja import ModelSchema, Router
from typing import List
from .models import Player


router = Router()


class GetPlayer(ModelSchema):
    class Config:
        model = Player
        model_fields = [
            "id",
            "first_name",
            "last_name",
            "team_name",
            "goals",
            "assists",
            "points",
            "picture",
        ]
        # arbitrary_types_allowed = True


@router.get("/", response=List[GetPlayer])
def list_events(request):
    return Player.objects.all()
