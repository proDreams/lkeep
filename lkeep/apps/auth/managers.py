"""
Проект: Lkeep
Автор: Иван Ашихмин
Год: 2025
Специально для проекта "Код на салфетке"
https://pressanybutton.ru/category/servis-na-fastapi/
"""

from fastapi import Depends, HTTPException
from sqlalchemy import insert, update
from sqlalchemy.exc import IntegrityError

from lkeep.apps.auth.schemas import CreateUser, UserReturnData
from lkeep.core.core_dependency.db_dependency import DBDependency
from lkeep.database.models import User


class UserManager:
    """
    Класс для управления пользователями.
    """

    def __init__(self, db: DBDependency = Depends(DBDependency)) -> None:
        """
        Инициализирует экземпляр класса.

        :param db: Зависимость от базы данных. По умолчанию используется Depends(DBDependency).
        :type db: DBDependency
        """
        self.db = db
        self.model = User

    async def create_user(self, user: CreateUser) -> UserReturnData:
        """
        Создает нового пользователя в базе данных.

        :param user: Объект с данными для создания пользователя.
        :type user: CreateUser
        :returns: Данные созданного пользователя.
        :rtype: UserReturnData
        :raises HTTPException: Если пользователь уже существует.
        """
        async with self.db.db_session() as session:
            query = insert(self.model).values(**user.model_dump()).returning(self.model)

            try:
                result = await session.execute(query)
            except IntegrityError:
                raise HTTPException(status_code=400, detail="User already exists.")

            await session.commit()

            user_data = result.scalar_one()
            return UserReturnData(**user_data.__dict__)

    async def confirm_user(self, email: str) -> None:
        """
        Асинхронный метод для подтверждения пользователя по электронной почте.

        :param email: Электронная почта пользователя, которого нужно подтвердить.
        :type email: str
        """
        async with self.db.db_session() as session:
            query = update(self.model).where(self.model.email == email).values(is_verified=True, is_active=True)
            await session.execute(query)
            await session.commit()
