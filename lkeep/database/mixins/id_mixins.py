"""
Проект: Lkeep
Автор: Иван Ашихмин
Год: 2025
Специально для проекта "Код на салфетке"
https://pressanybutton.ru/category/servis-na-fastapi/
"""

import uuid

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column


class IDMixin:
    """
    Класс-миксин для добавления уникального идентификатора к объектам.

    :ivar id: Уникальный идентификатор объекта.
    :type id: uuid.UUID
    """

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
