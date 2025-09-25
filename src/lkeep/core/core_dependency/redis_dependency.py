"""
Проект: Lkeep
Автор: Иван Ашихмин
Год: 2025
Специально для проекта "Код на салфетке"
https://pressanybutton.ru/category/servis-na-fastapi/
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from redis.asyncio import ConnectionPool, Redis

from lkeep.core.settings import settings


class RedisDependency:
    """
    Класс, предоставляющий инструменты для работы с Redis через асинхронный клиент.

    :ivar _url: URL подключения к Redis серверу.
    :type _url: str
    :ivar _pool: Пул соединений для управления соединениями с Redis.
    :type _pool: ConnectionPool
    """

    def __init__(self) -> None:
        """
        Инициализирует экземпляр класса для работы с Redis.
        """
        self._url = settings.redis_settings.redis_url
        self._pool: ConnectionPool = self._init_pool()

    def _init_pool(self) -> ConnectionPool:
        """
        Инициализирует пул соединений Redis.

        :returns: Пул соединений для работы с Redis.
        :rtype: ConnectionPool
        """
        return ConnectionPool.from_url(url=self._url, encoding="utf-8", decode_responses=True)

    @asynccontextmanager
    async def get_client(self) -> AsyncGenerator[Redis]:
        """
        Получает клиентскую сессию Redis для взаимодействия с базой данных.

        :returns: Асинхронный генератор клиента Redis.
        :rtype: AsyncGenerator[Redis, None]
        """
        redis_client = Redis(connection_pool=self._pool)
        try:
            yield redis_client
        finally:
            await redis_client.aclose()
