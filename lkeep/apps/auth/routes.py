"""
Проект: Lkeep
Автор: Иван Ашихмин
Год: 2025
Специально для проекта "Код на салфетке"
https://pressanybutton.ru/category/servis-na-fastapi/
"""

from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from lkeep.apps.auth.schemas import AuthUser, UserReturnData
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
