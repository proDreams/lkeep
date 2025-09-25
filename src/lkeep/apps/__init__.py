"""
Проект: Lkeep
Автор: Иван Ашихмин
Год: 2025
Специально для проекта "Код на салфетке"
https://pressanybutton.ru/category/servis-na-fastapi/
"""

from fastapi import APIRouter

from lkeep.apps.auth.routes import auth_router
from lkeep.apps.links.routes import links_router
from lkeep.apps.profile.routes import profile_router

apps_router = APIRouter(prefix="/api/v1")

apps_router.include_router(router=auth_router)
apps_router.include_router(router=profile_router)
apps_router.include_router(router=links_router)
