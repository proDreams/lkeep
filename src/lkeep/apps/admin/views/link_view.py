from typing import Any

from starlette.requests import Request
from starlette_admin import StringField
from starlette_admin.contrib.sqla import ModelView

from lkeep.database.models import Link


class LinkViewView(ModelView):
    fields = [
        "id",
        "full_link",
        "short_link",
        StringField("owner_id", label="owner_id", read_only=True),
    ]

    async def before_create(self, request: Request, data: dict[str, Any], link: Link):
        admin_user = request.state.user
        link.owner_id = admin_user["id"]
