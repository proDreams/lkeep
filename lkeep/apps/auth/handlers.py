"""
Проект: Lkeep
Автор: Иван Ашихмин
Год: 2025
Специально для проекта "Код на салфетке"
https://pressanybutton.ru/category/servis-na-fastapi/
"""

import datetime
import uuid

import jwt
from passlib.context import CryptContext

from lkeep.apps.auth.named_tuples import CreateTokenTuple
from lkeep.core.settings import settings


class AuthHandler:
    """
    Обрабатывает аутентификационные запросы и обеспечивает безопасность пользовательских данных.

    :ivar secret: Секретный ключ, используемый для дополнительной безопасности при генерации хешей.
    :type secret: str
    :ivar pwd_context: Контекст для использования bcrypt-алгоритма хеширования паролей.
    :type pwd_context: CryptContext
    """

    secret = settings.secret_key.get_secret_value()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def get_password_hash(self, password: str) -> str:
        """
        Генерирует хэш-значение пароля для безопасного сохранения и сравнения.

        :param password: Пароль пользователя, который нужно зашифровать.
        :type password: str
        :returns: Хешированный вариант пароля.
        :rtype: str
        """
        return self.pwd_context.hash(password)

    async def verify_password(self, raw_password: str, hashed_password: str) -> bool:
        """
        Проверяет соответствие введенного пароля захэшированному паролю.

        :param raw_password: Введенный пользователем пароль.
        :type raw_password: str
        :param hashed_password: Хэш, с которым сравнивается введенный пароль.
        :type hashed_password: str
        :returns: Логическое значение, указывающее на успешность проверки.
        :rtype: bool
        """
        return self.pwd_context.verify(raw_password, hashed_password)

    async def create_access_token(self, user_id: uuid.UUID | str) -> CreateTokenTuple:
        """
        Создаёт JWT-токен доступа для пользователя.

        :param user_id: Уникальный идентификатор пользователя (UUID).
        :type user_id: uuid.UUID
        :returns: Кортеж, содержащий закодированный JWT-токен и уникальный session_id.
        :rtype: CreateTokenTuple
        """
        expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=settings.access_token_expire)
        session_id = str(uuid.uuid4())

        data = {"exp": expire, "session_id": session_id, "user_id": str(user_id)}

        encoded_jwt = jwt.encode(payload=data, key=self.secret, algorithm="HS256")

        return CreateTokenTuple(encoded_jwt=encoded_jwt, session_id=session_id)
