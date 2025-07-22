import uuid
from typing import Any

from fastapi import Depends
from sqlalchemy import select, update

from lkeep.core.core_dependency.db_dependency import DBDependency
from lkeep.database.models import User


class ProfileManager:
    def __init__(self, db: DBDependency = Depends(DBDependency)) -> None:
        self.db = db
        self.user_model = User

    async def update_user_fields(self, user_id: uuid.UUID | str, **kwargs: Any) -> None:
        async with self.db.db_session() as session:
            query = update(self.user_model).where(self.user_model.id == user_id).values(**kwargs)

            await session.execute(query)

            await session.commit()

    async def get_user_hashed_password(self, user_id: uuid.UUID | str) -> str:
        async with self.db.db_session() as session:
            query = select(self.user_model.hashed_password).where(self.user_model.id == user_id)

            result = await session.execute(query)

            return result.scalar()
