"""
Проект: Lkeep
Автор: Иван Ашихмин
Год: 2025
Специально для проекта "Код на салфетке"
https://pressanybutton.ru/category/servis-na-fastapi/
"""

import uuid

from fastapi import Depends, HTTPException
from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError

from lkeep.apps.auth.schemas import CreateUser, GetUserWithIDAndEmail, UserReturnData
from lkeep.core.core_dependency.db_dependency import DBDependency
from lkeep.core.core_dependency.redis_dependency import RedisDependency
from lkeep.database.models import User


class UserManager:
    """
    Класс для управления пользователями.
    """

    def __init__(
        self, db: DBDependency = Depends(DBDependency), redis: RedisDependency = Depends(RedisDependency)
    ) -> None:
        """
        Инициализирует экземпляр класса.

        :param db: Зависимость для базы данных. По умолчанию используется Depends(DBDependency).
        :type db: DBDependency
        :param redis: Зависимость для Redis. По умолчанию используется Depends(RedisDependency).
        :type redis: RedisDependency
        """
        self.db = db
        self.model = User
        self.redis = redis

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

    async def get_user_by_email(self, email: str) -> GetUserWithIDAndEmail | None:
        """
        Возвращает пользователя по указанному адресу электронной почты.

        :param email: Адрес электронной почты пользователя для поиска.
        :type email: str
        :return: Объект пользователя с полями id и email, если пользователь найден; None в противном случае.
        :rtype: GetUserWithIDAndEmail | None
        """
        async with self.db.db_session() as session:
            query = select(self.model.id, self.model.email, self.model.hashed_password).where(self.model.email == email)

            result = await session.execute(query)
            user = result.mappings().first()

            if user:
                return GetUserWithIDAndEmail(**user)

            return None

    async def store_access_token(self, token: str, user_id: uuid.UUID | str, session_id: str) -> None:
        """
        Сохраняет токен доступа в хранилище (Redis).

        :param token: Токен доступа для сохранения.
        :type token: str
        :param user_id: Идентификатор пользователя, которому принадлежит токен.
        :type user_id: uuid.UUID
        :param session_id: Идентификатор сессии, связанной с токеном.
        :type session_id: str
        """
        async with self.redis.get_client() as client:
            await client.set(f"{user_id}:{session_id}", token)
