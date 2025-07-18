"""
Проект: Lkeep
Автор: Иван Ашихмин
Год: 2025
Специально для проекта "Код на салфетке"
https://pressanybutton.ru/category/servis-na-fastapi/
"""

from celery import Celery

from lkeep.core.settings import settings

celery_app = Celery(main="lkeep", broker=settings.redis_settings.redis_url, backend=settings.redis_settings.redis_url)

celery_app.autodiscover_tasks(packages=["lkeep.apps"])
