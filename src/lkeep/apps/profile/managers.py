"""
Проект: Lkeep
Автор: Иван Ашихмин
Год: 2025
Специально для проекта "Код на салфетке"
https://pressanybutton.ru/category/servis-na-fastapi/
"""

import uuid
from typing import Any

from fastapi import Depends
from sqlalchemy import select, update

from lkeep.core.core_dependency.db_dependency import DBDependency
from lkeep.database.models import User


class ProfileManager:
    """
    Менеджер для работы с данными профиля в базе данных.
    """

    def __init__(self, db: DBDependency = Depends(DBDependency)) -> None:
        """
        Инициализирует менеджер с зависимостью доступа к базе данных.

        :param db: Провайдер асинхронных сессий базы данных.
        :type db: DBDependency
        """
        self.db = db
        self.user_model = User

    async def update_user_fields(self, user_id: uuid.UUID | str, **kwargs: Any) -> None:
        """
        Обновляет выбранные поля пользователя по его идентификатору.

        :param user_id: Идентификатор пользователя, данные которого нужно изменить.
        :type user_id: uuid.UUID | str
        :param kwargs: Поля и значения, подлежащие обновлению.
        :type kwargs: Any
        :returns: None
        """
        async with self.db.db_session() as session:
            query = update(self.user_model).where(self.user_model.id == user_id).values(**kwargs)

            await session.execute(query)

            await session.commit()

    async def get_user_hashed_password(self, user_id: uuid.UUID | str) -> str:
        """
        Возвращает хешированный пароль пользователя.

        :param user_id: Идентификатор пользователя для поиска.
        :type user_id: uuid.UUID | str
        :returns: Хеш текущего пароля пользователя.
        :rtype: str
        """
        async with self.db.db_session() as session:
            query = select(self.user_model.hashed_password).where(self.user_model.id == user_id)

            result = await session.execute(query)

            return result.scalar()
