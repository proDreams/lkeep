"""
Проект: Lkeep
Автор: Иван Ашихмин
Год: 2025
Специально для проекта "Код на салфетке"
https://pressanybutton.ru/category/servis-na-fastapi/
"""

import uuid
from datetime import datetime

from pydantic import BaseModel


class BaseFullLink(BaseModel):
    """
    Базовая схема, содержащая полный адрес ссылки.
    """

    full_link: str


class DeleteLinkSchema(BaseModel):
    """
    Схема для удаления ссылки по идентификатору.
    """

    id: uuid.UUID


class LinkSchema(BaseFullLink, DeleteLinkSchema):
    """
    Полная схема ссылки с коротким адресом и метаданными.
    """

    short_link: str
    created_at: datetime


class GetLinkSchema(BaseFullLink):
    """Схема ответа при получении полной ссылки по сокращенному адресу."""


class CreateLinkSchema(BaseFullLink):
    """Схема запроса на создание новой ссылки."""
