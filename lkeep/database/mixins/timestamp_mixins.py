"""
Проект: Lkeep
Автор: Иван Ашихмин
Год: 2025
Специально для проекта "Код на салфетке"
https://pressanybutton.ru/category/servis-na-fastapi/
"""

import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class CreatedAtMixin:
    """
    Класс-миксин, добавляющий атрибут created_at для отслеживания времени создания объектов.

    :ivar created_at: Время создания объекта.
    :type created_at: datetime.datetime
    """

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=datetime.datetime.now,
    )


class UpdatedAtMixin:
    """
    Класс-миксин, добавляющий атрибут `updated_at`, который автоматически обновляется при каждом изменении записи.

    :ivar updated_at: Время последнего обновления записи.
    :type updated_at: Mapped[datetime.datetime]
    """

    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class TimestampsMixin(CreatedAtMixin, UpdatedAtMixin):
    """
    Класс-миксин для добавления временных меток создания и обновления в классы.

    :ivar created_at: Время создания записи.
    :type created_at: datetime.datetime
    :ivar updated_at: Время последнего обновления записи.
    :type updated_at: datetime.datetime
    """

    pass
