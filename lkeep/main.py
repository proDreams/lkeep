"""
Проект: Lkeep
Автор: Иван Ашихмин
Год: 2025
Специально для проекта "Код на салфетке"
https://pressanybutton.ru/category/servis-na-fastapi/
"""

import uvicorn
from fastapi import FastAPI

from lkeep.apps import apps_router

app = FastAPI()

app.include_router(router=apps_router)


def start():
    uvicorn.run(app="lkeep.main:app", reload=True)
