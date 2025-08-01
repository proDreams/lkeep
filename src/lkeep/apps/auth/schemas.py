"""
Проект: Lkeep
Автор: Иван Ашихмин
Год: 2025
Специально для проекта "Код на салфетке"
https://pressanybutton.ru/category/servis-na-fastapi/
"""

import datetime
import uuid
from typing import Annotated

from pydantic import BaseModel, EmailStr, StringConstraints


class GetUserByID(BaseModel):
    """
    Класс для получения пользователя по его уникальному идентификатору (ID).

    :ivar id: Уникальный идентификатор пользователя, может быть представлен как объект типа uuid.UUID или строкой.
    :type id: uuid.UUID | str
    """

    id: uuid.UUID | str


class GetUserByEmail(BaseModel):
    """
    Класс для поиска пользователя по электронной почте.

    :ivar email: Электронная почта пользователя.
    :type email: EmailStr
    """

    email: EmailStr


class UserVerifySchema(GetUserByID, GetUserByEmail):
    """
    Класс для валидации данных пользователя.

    Данный класс наследует методы из классов GetUserByID и GetUserByEmail,
    что позволяет использовать их функциональность для проверки данных пользователя.
    """

    session_id: uuid.UUID | str | None = None


class AuthUser(GetUserByEmail):
    """
    Класс для регистрации пользователя, наследующий класс GetUserByEmail.

    :ivar password: Пароль пользователя.
    :type password: str
    """

    password: Annotated[str, StringConstraints(min_length=8, max_length=128)]


class CreateUser(GetUserByEmail):
    """
    Класс для создания пользователя.

    :ivar hashed_password: Хэшированный пароль пользователя.
    :type hashed_password: str
    """

    hashed_password: str


class GetUserWithIDAndEmail(GetUserByID, CreateUser):
    """
    Класс для получения пользователя по его ID и email.

    :ivar id: Уникальный идентификатор пользователя.
    :type id: int
    :ivar email: Адрес электронной почты пользователя.
    :type email: str
    :ivar hashed_password: Хэшированный пароль пользователя.
    :type hashed_password: str
    """

    pass


class UserReturnData(GetUserByID, GetUserByEmail):
    """
    Класс для представления данных пользователя, возвращаемых из API.

    :ivar is_active: Статус активности пользователя.
    :type is_active: bool
    :ivar is_verified: Статус верификации пользователя.
    :type is_verified: bool
    :ivar is_superuser: Флаг, указывающий на наличие привилегий суперпользователя.
    :type is_superuser: bool
    :ivar created_at: Временная метка создания записи о пользователе.
    :type created_at: datetime.datetime
    :ivar updated_at: Временная метка последнего обновления записи о пользователе.
    :type updated_at: datetime.datetime
    """

    is_active: bool
    is_verified: bool
    is_superuser: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
