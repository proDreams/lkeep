"""
Проект: Lkeep
Автор: Иван Ашихмин
Год: 2025
Специально для проекта "Код на салфетке"
https://pressanybutton.ru/category/servis-na-fastapi/
"""

from fastapi import APIRouter, Depends
from starlette import status

from lkeep.apps.auth.schemas import RegisterUser, UserReturnData
from lkeep.apps.auth.services import UserService

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post(path="/register", response_model=UserReturnData, status_code=status.HTTP_201_CREATED)
async def registration(user: RegisterUser, service: UserService = Depends(UserService)) -> UserReturnData:
    """
    Регистрация нового пользователя.

    :param user: Данные нового пользователя, который нужно зарегистрировать.
    :type user: RegisterUser
    :param service: Сервис для взаимодействия с пользователями.
    :type service: UserService
    :returns: Данные зарегистрированного пользователя.
    :rtype: UserReturnData
    :raises HTTPException 400: Если данные пользователя некорректны.
    """
    return await service.register_user(user=user)
