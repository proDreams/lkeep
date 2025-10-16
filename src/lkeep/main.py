"""
Проект: Lkeep
Автор: Иван Ашихмин
Год: 2025
Специально для проекта "Код на салфетке"
https://pressanybutton.ru/category/servis-na-fastapi/
"""

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from lkeep.apps import apps_router
from lkeep.apps.admin.admin_base import setup_admin

app = FastAPI()

app.include_router(router=apps_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],  # TODO: ЗАМЕНИТЬ ПОТОМ НА ДОМЕН
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_admin(app=app)


def start():
    """
    Запускает локальный сервер приложения с поддержкой автоматической перезагрузки.

    :returns: None
    """
    uvicorn.run(app="lkeep.main:app", reload=True)
