"""
Проект: Lkeep
Автор: Иван Ашихмин
Год: 2025
Специально для проекта "Код на салфетке"
https://pressanybutton.ru/category/servis-na-fastapi/
"""

from fastapi import HTTPException
from starlette import status
from starlette.requests import Request


async def get_token_from_cookies(request: Request) -> str:
    """
    Получает токен из куки запроса.

    :param request: Объект HTTP-запроса.
    :type request: Request
    :return: Токен из cookies.
    :rtype: str
    :raises HTTPException: Если в запросе отсутствует cookie с ключом "Authorization".
    """
    token = request.cookies.get("Authorization")
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    return token
