"""
Проект: Lkeep
Автор: Иван Ашихмин
Год: 2025
Специально для проекта "Код на салфетке"
https://pressanybutton.ru/category/servis-na-fastapi/
"""

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    """
    Класс для настройки параметров подключения к базе данных.

    :ivar db_name: Имя базы данных.
    :type db_name: str
    :ivar db_user: Логин пользователя для доступа к базе данных.
    :type db_user: str
    :ivar db_password: Пароль пользователя для доступа к базе данных. Значение хранится в зашифрованном виде.
    :type db_password: SecretStr
    :ivar db_host: Адрес хоста, на котором размещена база данных.
    :type db_host: str
    :ivar db_port: Порт, по которому осуществляется подключение к базе данных.
    :type db_port: int
    :ivar db_echo: Флаг для вывода отладочной информации о запросах к базе данных.
    :type db_echo: bool
    """

    db_name: str
    db_user: str
    db_password: SecretStr
    db_host: str
    db_port: int
    db_echo: bool

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf8", extra="ignore")

    @property
    def db_url(self):
        """
        Свойство, возвращающее строку подключения к базе данных PostgreSQL.

        :returns: Строка подключения к базе данных.
        :rtype: str
        """
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password.get_secret_value()}@{self.db_host}:{self.db_port}/{self.db_name}"


class EmailSettings(BaseSettings):
    """
    Настройки для электронной почты.

    :ivar email_host: Адрес SMTP-сервера.
    :type email_host: str
    :ivar email_port: Порт, используемый для подключения к SMTP-серверу.
    :type email_port: int
    :ivar email_username: Имя пользователя для аутентификации на электронной почтовом сервере.
    :type email_username: str
    :ivar email_password: Пароль пользователя, скрытый через `SecretStr` для обеспечения безопасности.
    :type email_password: SecretStr
    :model_config: Конфигурация settings, которая указывает на файл окружения и его кодировку.
    :type model_config: SettingsConfigDict
    """

    email_host: str
    email_port: int
    email_username: str
    email_password: SecretStr

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf8", extra="ignore")


class RedisSettings(BaseSettings):
    """
    Класс для настройки соединения с Redis.

    :ivar redis_host: Хост, на котором размещается Redis-сервер.
    :type redis_host: str
    :ivar redis_port: Порт, через который происходит соединение с Redis-сервером.
    :type redis_port: int
    :ivar redis_db: Номер базы данных для использования в Redis.
    :type redis_db: int
    """

    redis_host: str
    redis_port: int
    redis_db: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf8", extra="ignore")

    @property
    def redis_url(self):
        """
        Получает URL для подключения к Redis.

        :returns: Строка с URL для подключения к Redis в формате `redis://<хост>:<порт>/<база данных>`.
        :rtype: str
        """
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"


class Settings(BaseSettings):
    """
    Класс для хранения настроек приложения.

    :ivar db_settings: Настройки для работы с базой данных.
    :type db_settings: DBSettings
    :ivar email_settings: Настройки для отправки электронной почты.
    :type email_settings: EmailSettings
    :ivar redis_settings: Настройки для работы с Redis.
    :type redis_settings: RedisSettings
    :ivar secret_key: Секретный ключ приложения.
    :type secret_key: SecretStr
    :ivar templates_dir: Путь к директории шаблонов.
    :type templates_dir: str
    :ivar frontend_url: Адрес фронтенд-приложения.
    :type frontend_url: str
    :ivar access_token_expire: Срок жизни JWT-токена
    :type access_token_expire: int
    :ivar link_length: Максимальная длина короткой ссылки
    :type link_length: int
    """

    db_settings: DBSettings = DBSettings()
    email_settings: EmailSettings = EmailSettings()
    redis_settings: RedisSettings = RedisSettings()
    secret_key: SecretStr
    templates_dir: str = "templates"
    frontend_url: str
    access_token_expire: int
    domain: str
    link_length: int = 12

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf8", extra="ignore")


settings = Settings()
