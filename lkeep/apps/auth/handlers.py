from passlib.context import CryptContext

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
