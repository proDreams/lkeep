"""
Проект: Lkeep
Автор: Иван Ашихмин
Год: 2025
Специально для проекта "Код на салфетке"
https://pressanybutton.ru/category/servis-na-fastapi/
"""

import uuid

from fastapi import Depends
from sqlalchemy import delete, insert, select

from lkeep.apps.links.schemas import GetLinkSchema, LinkSchema
from lkeep.core.core_dependency.db_dependency import DBDependency
from lkeep.database.models import Link


class LinksManager:
    """
    Менеджер для выполнения операций над ссылками в базе данных.
    """

    def __init__(self, db: DBDependency = Depends(DBDependency)) -> None:
        """
        Инициализирует менеджер с зависимостью доступа к базе данных.

        :param db: Объект для получения асинхронных сессий с базой данных.
        :type db: DBDependency
        """
        self.db = db
        self.link_model = Link

    async def get_link(self, short_link: str) -> GetLinkSchema | None:
        """
        Возвращает полную ссылку по короткому идентификатору.

        :param short_link: Сокращенный идентификатор ссылки.
        :type short_link: str
        :returns: Найденная ссылка или None, если запись отсутствует.
        :rtype: GetLinkSchema | None
        """
        async with self.db.db_session() as session:
            query = select(self.link_model.full_link).where(self.link_model.short_link == short_link)

            result = await session.execute(query)
            link = result.scalar_one_or_none()

            if link:
                return GetLinkSchema(full_link=link)

            return None

    async def get_links(self, user_id: uuid.UUID) -> list[LinkSchema]:
        """
        Получает список ссылок, принадлежащих пользователю.

        :param user_id: Идентификатор владельца ссылок.
        :type user_id: uuid.UUID
        :returns: Список ссылок пользователя.
        :rtype: list[LinkSchema]
        """
        async with self.db.db_session() as session:
            query = select(self.link_model).where(self.link_model.owner_id == user_id)

            result = await session.execute(query)
            links = result.scalars().all()

            return [LinkSchema.model_validate(link, from_attributes=True) for link in links]

    async def create_link(self, full_link: str, user_id: uuid.UUID, short_link: str) -> LinkSchema:
        """
        Создает новую ссылку и возвращает сохраненную запись.

        :param full_link: Полный адрес, который требуется сократить.
        :type full_link: str
        :param user_id: Идентификатор владельца ссылки.
        :type user_id: uuid.UUID
        :param short_link: Сгенерированное короткое представление ссылки.
        :type short_link: str
        :returns: Созданная ссылка с заполненными полями.
        :rtype: LinkSchema
        """
        async with self.db.db_session() as session:
            query = (
                insert(self.link_model)
                .values(full_link=full_link, short_link=short_link, owner_id=user_id)
                .returning(self.link_model)
            )

            result = await session.execute(query)
            await session.commit()
            link = result.scalar()

            return LinkSchema.model_validate(link, from_attributes=True)

    async def get_link_owner(self, link_id: uuid.UUID) -> uuid.UUID | None:
        """
        Возвращает идентификатор владельца ссылки.

        :param link_id: Идентификатор ссылки.
        :type link_id: uuid.UUID
        :returns: Идентификатор владельца или None, если ссылка не найдена.
        :rtype: uuid.UUID | None
        """
        async with self.db.db_session() as session:
            query = select(self.link_model.owner_id).where(self.link_model.id == link_id)

            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def delete_link(self, link_id: uuid.UUID) -> None:
        """
        Удаляет ссылку по ее идентификатору.

        :param link_id: Идентификатор ссылки, которую требуется удалить.
        :type link_id: uuid.UUID
        :returns: None
        """
        async with self.db.db_session() as session:
            query = delete(self.link_model).where(self.link_model.id == link_id)

            await session.execute(query)
            await session.commit()
