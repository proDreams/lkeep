"""
Проект: Lkeep
Автор: Иван Ашихмин
Год: 2025
Специально для проекта "Код на салфетке"
https://pressanybutton.ru/category/servis-na-fastapi/
"""

from typing import Annotated

from pydantic import BaseModel, EmailStr, StringConstraints


class ChangeEmailRequest(BaseModel):
    """
    Схема запроса на изменение электронной почты пользователя.
    """

    new_email: EmailStr


class ChangePasswordRequest(BaseModel):
    """
    Схема запроса на обновление пароля пользователя.
    """

    old_password: Annotated[str, StringConstraints(min_length=8, max_length=128)]
    new_password: Annotated[str, StringConstraints(min_length=8, max_length=128)]
