from fastapi import FastAPI
from starlette_admin.contrib.sqla import Admin

from lkeep.apps.admin.admin_auth import get_admin_auth_provider
from lkeep.apps.admin.views.link_view import LinkViewView
from lkeep.apps.admin.views.user_view import UserView
from lkeep.core.core_dependency.db_dependency import get_db_engine
from lkeep.database.models import Link, User


def setup_admin(app: FastAPI) -> None:
    admin = Admin(engine=get_db_engine(), title="Lkeep Admin", auth_provider=get_admin_auth_provider())

    admin.add_view(UserView(User))
    admin.add_view(LinkViewView(Link))

    admin.mount_to(app=app)
