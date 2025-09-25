"""
Проект: Lkeep
Автор: Иван Ашихмин
Год: 2025
Специально для проекта "Код на салфетке"
https://pressanybutton.ru/category/servis-na-fastapi/
"""

import secrets

from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status

from lkeep.apps.auth.schemas import UserVerifySchema
from lkeep.apps.links.managers import LinksManager
from lkeep.apps.links.schemas import (
    CreateLinkSchema,
    DeleteLinkSchema,
    GetLinkSchema,
    LinkSchema,
)
from lkeep.core.settings import settings


class LinksService:
    """
    Сервисный слой для работы с пользовательскими ссылками.
    """

    def __init__(self, manager: LinksManager = Depends(LinksManager)) -> None:
        """
        Создает сервис со связанным менеджером ссылок.

        :param manager: Менеджер, выполняющий операции с базой данных.
        :type manager: LinksManager
        """
        self.manager = manager

    async def get_link(self, short_link: str) -> GetLinkSchema | None:
        """
        Получает полную ссылку по ее короткому представлению.

        :param short_link: Сокращенный идентификатор ссылки.
        :type short_link: str
        :returns: Полная ссылка или None, если запись отсутствует.
        :rtype: GetLinkSchema | None
        """
        return await self.manager.get_link(short_link=short_link)

    async def get_links(self, user: UserVerifySchema) -> list[LinkSchema]:
        """
        Возвращает все ссылки, принадлежащие пользователю.

        :param user: Данные авторизованного пользователя.
        :type user: UserVerifySchema
        :returns: Список ссылок пользователя.
        :rtype: list[LinkSchema]
        """
        return await self.manager.get_links(user_id=user.id)

    async def create_link(self, link_data: CreateLinkSchema, user: UserVerifySchema) -> LinkSchema:
        """
        Создает новую сокращенную ссылку для пользователя.

        :param link_data: Данные запроса с полным адресом ссылки.
        :type link_data: CreateLinkSchema
        :param user: Пользователь, которому будет принадлежать ссылка.
        :type user: UserVerifySchema
        :returns: Созданная запись о ссылке.
        :rtype: LinkSchema
        """
        link_length = settings.link_length

        while True:
            short_link = secrets.token_urlsafe(link_length)[:link_length]
            try:
                return await self.manager.create_link(
                    full_link=link_data.full_link, user_id=user.id, short_link=short_link
                )
            except IntegrityError:
                continue

    async def delete_link(self, link_data: DeleteLinkSchema, user: UserVerifySchema) -> None:
        """
        Удаляет ссылку пользователя после проверки владельца.

        :param link_data: Данные с идентификатором ссылки для удаления.
        :type link_data: DeleteLinkSchema
        :param user: Пользователь, запрашивающий удаление.
        :type user: UserVerifySchema
        :raises HTTPException: Если пользователь не является владельцем ссылки.
        :returns: None
        """
        link_owner = await self.manager.get_link_owner(link_id=link_data.id)

        if link_owner and link_owner == user.id:
            await self.manager.delete_link(link_id=link_data.id)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong link owner")
