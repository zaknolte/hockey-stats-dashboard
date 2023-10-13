from ninja import ModelSchema, Router
from typing import List
from .models import PlayerInfo


router = Router()


class PlayerInfoSchema(ModelSchema):
    class Config:
        model = PlayerInfo
        model_fields = [
            "id",
            "first_name",
            "last_name",
            "team_name",
            "picture",
        ]
        # arbitrary_types_allowed = True


@router.get("/", response=List[PlayerInfoSchema])
def list_events(request):
    return PlayerInfo.objects.all()
