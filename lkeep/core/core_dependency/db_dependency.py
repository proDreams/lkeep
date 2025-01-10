from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class DBDependency:
    """
    Класс для управления зависимостями базы данных, используя SQLAlchemy.
    """

    def __init__(self, db_url: str, db_echo: bool) -> None:
        """
        Инициализирует экземпляр класса, отвечающего за взаимодействие с асинхронной базой данных.

        :param db_url: URL для подключения к базе данных.
        :type db_url: str
        :param db_echo: Флаг, определяющий вывод подробных логов при взаимодействии с базой данных.
        :type db_echo: bool
        """
        self._engine = create_async_engine(url=db_url, echo=db_echo)
        self._session_factory = async_sessionmaker(bind=self._engine, expire_on_commit=False, autocommit=False)

    @property
    def db_session(self) -> async_sessionmaker[AsyncSession]:
        """
        Декоратор для создания асинхронной сессии базы данных.

        :returns: Возвращает фабрику асинхронных сессий.
        :rtype: async_sessionmaker[AsyncSession]
        """
        return self._session_factory
