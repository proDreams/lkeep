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


class Settings(BaseSettings):
    """
    Класс Settings используется для хранения настроек приложения.

    :ivar db_settings: Экземпляр класса DBSettings, содержащий настройки базы данных.
    :type db_settings: DBSettings
    """

    db_settings: DBSettings = DBSettings()


settings = Settings()
