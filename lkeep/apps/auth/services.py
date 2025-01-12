"""
Проект: Lkeep
Автор: Иван Ашихмин
Год: 2025
Специально для проекта "Код на салфетке"
https://pressanybutton.ru/category/servis-na-fastapi/
"""

from fastapi import Depends

from lkeep.apps.auth.handlers import AuthHandler
from lkeep.apps.auth.managers import UserManager
from lkeep.apps.auth.schemas import CreateUser, RegisterUser, UserReturnData


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

    async def register_user(self, user: RegisterUser) -> UserReturnData:
        """
        Регистрирует нового пользователя в системе.

        :param user: Данные для регистрации пользователя.
        :type user: RegisterUser
        :return: Данные зарегистрированного пользователя.
        :rtype: UserReturnData
        """
        hashed_password = await self.handler.get_password_hash(user.password)

        new_user = CreateUser(email=user.email, hashed_password=hashed_password)

        return await self.manager.create_user(user=new_user)
