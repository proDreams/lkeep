"""
Проект: Lkeep
Автор: Иван Ашихмин
Год: 2025
Специально для проекта "Код на салфетке"
https://pressanybutton.ru/category/servis-na-fastapi/
"""

from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from lkeep.apps.auth.depends import get_current_user
from lkeep.apps.auth.schemas import AuthUser, UserReturnData, UserVerifySchema
from lkeep.apps.auth.services import UserService

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post(path="/register", response_model=UserReturnData, status_code=status.HTTP_201_CREATED)
async def registration(user: AuthUser, service: UserService = Depends(UserService)) -> UserReturnData:
    """
    Регистрация нового пользователя.

    :param user: Данные нового пользователя, который нужно зарегистрировать.
    :type user: AuthUser
    :param service: Сервис для взаимодействия с пользователями.
    :type service: UserService
    :returns: Данные зарегистрированного пользователя.
    :rtype: UserReturnData
    :raises HTTPException 400: Если данные пользователя некорректны.
    """
    return await service.register_user(user=user)


@auth_router.get(path="/register_confirm", status_code=status.HTTP_200_OK)
async def confirm_registration(token: str, service: UserService = Depends(UserService)) -> dict[str, str]:
    """
    Подтверждает регистрацию пользователя по ссылке.

    :param token: Токен подтверждения регистрации, полученный после отправки на электронную почту.
    :type token: str
    :param service: Сервис для взаимодействия с пользователями.
    :raises HTTPException: Если токен недействителен или срок действия истек.
    :return: Словарь с сообщением о успешной подтверждении электронной почты.
    :rtype: dict[str, str]
    """
    await service.confirm_user(token=token)

    return {"message": "Электронная почта подтверждена"}


@auth_router.post(path="/login", status_code=status.HTTP_200_OK)
async def login(user: AuthUser, service: UserService = Depends(UserService)) -> JSONResponse:
    """
    Вход пользователя в систему.

    :param user: Объект данных пользователя для входа.
    :type user: AuthUser
    :param service: Сервисный объект для управления пользователями.
    :type service: UserService
    :returns: JSON-ответ с токеном доступа в Cookies, если вход выполнен успешно.
    :rtype: JSONResponse
    :raises HTTPException: Если учетные данные не верны или произошла другая ошибка при входе.
    """
    return await service.login_user(user=user)


@auth_router.get(path="/logout", status_code=status.HTTP_200_OK)
async def logout(
    user: Annotated[UserVerifySchema, Depends(get_current_user)], service: UserService = Depends(UserService)
) -> JSONResponse:
    """
    Описание функции logout.

    :param user: Текущий авторизованный пользователь.
    :type user: UserVerifySchema
    :param service: Сервис для управления пользователями.
    :type service: UserService
    :returns: JSON-ответ, содержащий результат логаута.
    :rtype: JSONResponse
    """
    return await service.logout_user(user=user)


@auth_router.get(path="/get-user", status_code=status.HTTP_200_OK, response_model=UserVerifySchema)
async def get_auth_user(user: Annotated[UserVerifySchema, Depends(get_current_user)]) -> UserVerifySchema:
    """
    Возвращает информацию об авторизованном пользователе.

    :param user: Информация о пользователе, полученная с помощью механизма аутентификации.
    :type user: UserVerifySchema
    :return: Схема данных пользователя, содержащая необходимую информацию для работы системы.
    :rtype: UserVerifySchema

    :raises HTTPException 401: Если пользователь не авторизован и попытка получить доступ к защищенному ресурсу.
    """
    return user
