"""
Проект: Lkeep
Автор: Иван Ашихмин
Год: 2025
Специально для проекта "Код на салфетке"
https://pressanybutton.ru/category/servis-na-fastapi/
"""

from fastapi import Depends, HTTPException
from itsdangerous import BadSignature, URLSafeTimedSerializer

from lkeep.apps.auth.handlers import AuthHandler
from lkeep.apps.auth.managers import UserManager
from lkeep.apps.auth.schemas import CreateUser, RegisterUser, UserReturnData
from lkeep.apps.auth.tasks import send_confirmation_email
from lkeep.core.settings import settings


class UserService:
    """
    Класс для управления пользователями.
    """

    def __init__(
        self, manager: UserManager = Depends(UserManager), handler: AuthHandler = Depends(AuthHandler)
    ) -> None:
        """
        Инициализирует экземпляр класса, используя зависимости для управления пользователями и авторизации.

        :param manager: Управитель пользователей, отвечающий за CRUD-операции над пользователями.
        :type manager: UserManager
        :param handler: Обработчик аутентификации и авторизации, который используется для проверки доступа к ресурсам.
        :type handler: AuthHandler
        """
        self.manager = manager
        self.handler = handler
        self.serializer = URLSafeTimedSerializer(secret_key=settings.secret_key.get_secret_value())

    async def register_user(self, user: RegisterUser) -> UserReturnData:
        """
        Регистрирует нового пользователя в системе.

        :param user: Информация о пользователе, который нужно зарегистрировать.
        :type user: RegisterUser
        :returns: Данные о созданном пользователе.
        :rtype: UserReturnData
        """
        hashed_password = await self.handler.get_password_hash(user.password)

        new_user = CreateUser(email=user.email, hashed_password=hashed_password)

        user_data = await self.manager.create_user(user=new_user)

        confirmation_token = self.serializer.dumps(user_data.email)
        send_confirmation_email.delay(to_email=user_data.email, token=confirmation_token)

        return user_data

    async def confirm_user(self, token: str) -> None:
        """
        Подтверждает пользователя по переданному токену.

        :param token: Токен для подтверждения пользователя.
        :type token: str
        :raises HTTPException: Если токен неверный или просроченный.
        """
        try:
            email = self.serializer.loads(token, max_age=3600)
        except BadSignature:
            raise HTTPException(status_code=400, detail="Неверный или просроченный токен")

        await self.manager.confirm_user(email=email)
