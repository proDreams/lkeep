"""
Проект: Lkeep
Автор: Иван Ашихмин
Год: 2025
Специально для проекта "Код на салфетке"
https://pressanybutton.ru/category/servis-na-fastapi/
"""

import uuid
from typing import Annotated

from fastapi import Depends, HTTPException
from starlette import status

from lkeep.apps.auth.handlers import AuthHandler
from lkeep.apps.auth.managers import UserManager
from lkeep.apps.auth.schemas import UserVerifySchema
from lkeep.apps.auth.utils import get_token_from_cookies


async def get_current_user(
    token: Annotated[str, Depends(get_token_from_cookies)],
    handler: AuthHandler = Depends(AuthHandler),
    manager: UserManager = Depends(UserManager),
) -> UserVerifySchema:
    """
    Получает текущего пользователя из токена аутентификации.

    :param token: Токен аутентификации, полученный из куки.
    :type token: str
    :param handler: Обработчик аутентификации, использующийся для декодирования токена.
    :type handler: AuthHandler
    :param manager: Менеджер пользователей, используется для проверки и получения данных о пользователе.
    :type manager: UserManager
    :returns: Схема с информацией о текущем пользователе.
    :rtype: UserVerifySchema
    :raises HTTPException: Если токен невалиден или пользователь не найден.
    """
    decoded_token = await handler.decode_access_token(token=token)
    user_id = str(decoded_token.get("user_id"))
    session_id = str(decoded_token.get("session_id"))

    if not await manager.get_access_token(user_id=user_id, session_id=session_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")

    user = await manager.get_user_by_id(user_id=uuid.UUID(user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    user.session_id = session_id

    return user
