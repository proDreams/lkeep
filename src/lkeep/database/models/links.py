"""
Проект: Lkeep
Автор: Иван Ашихмин
Год: 2025
Специально для проекта "Код на салфетке"
https://pressanybutton.ru/category/servis-na-fastapi/
"""

from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from lkeep.database.mixins.id_mixins import IDMixin
from lkeep.database.mixins.timestamp_mixins import CreatedAtMixin
from lkeep.database.models import Base


class Link(IDMixin, CreatedAtMixin, Base):
    """
    Модель сокращенной ссылки с указанием владельца.

    :ivar full_link: Полная ссылка
    :type full_link: str
    :ivar short_link: Сокращённая ссылка
    :type short_link: str
    :ivar owner_id: Создатель ссылки
    :type owner_id: UUID
    """

    full_link: Mapped[str] = mapped_column(String)
    short_link: Mapped[str] = mapped_column(String(12), unique=True, index=True)
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
