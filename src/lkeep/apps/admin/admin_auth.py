from fastapi import HTTPException
from pydantic import EmailStr, ValidationError
from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AuthProvider
from starlette_admin.exceptions import LoginFailed

from lkeep.apps.auth.handlers import AuthHandler
from lkeep.apps.auth.managers import UserManager
from lkeep.apps.auth.schemas import AuthUser, GetUserByID
from lkeep.apps.auth.utils import get_token_from_cookies
from lkeep.core.core_dependency.db_dependency import DBDependency
from lkeep.core.core_dependency.redis_dependency import RedisDependency
from lkeep.core.settings import settings


class AdminAuthProvider(AuthProvider):
    def __init__(self, handler: AuthHandler, manager: UserManager):
        super().__init__()
        self.handler = handler
        self.manager = manager

    async def is_authenticated(self, request: Request) -> bool:
        try:
            token = await get_token_from_cookies(request=request)
            decoded_token = await self.handler.decode_access_token(token=token)
        except HTTPException:
            return False

        user_id = str(decoded_token.get("user_id"))
        session_id = str(decoded_token.get("session_id"))

        if not await self.manager.get_access_token(user_id=user_id, session_id=session_id):
            return False

        request.state.user = {"id": user_id, "session_id": session_id}
        return True

    async def login(
        self, email: EmailStr, password: str, remember_me: bool, request: Request, response: Response
    ) -> Response:
        try:
            auth_data = AuthUser(email=email, password=password)
        except ValidationError:
            raise LoginFailed(msg="Invalid email or password")
        exist_user = await self.manager.get_user_by_email_for_admin(email=auth_data.email)

        if (
            exist_user is None
            or not exist_user.is_superuser
            or not await self.handler.verify_password(
                hashed_password=exist_user.hashed_password, raw_password=auth_data.password
            )
        ):
            raise LoginFailed(msg="Invalid credentials")

        token, session_id = await self.handler.create_access_token(user_id=exist_user.id)

        await self.manager.store_access_token(token=token, user_id=exist_user.id, session_id=session_id)

        response.set_cookie(key="Authorization", value=token, httponly=True, max_age=settings.access_token_expire)

        return response

    async def logout(self, request: Request, response: Response) -> Response:
        response.delete_cookie("Authorization")

        user = request.state.user

        await self.manager.revoke_access_token(user_id=user["id"], session_id=user["session_id"])

        return response

    def get_admin_user(self, request: Request) -> GetUserByID:
        return GetUserByID(**request.state.user)


def get_admin_auth_provider() -> AdminAuthProvider:
    manager = UserManager(db=DBDependency(), redis=RedisDependency())
    return AdminAuthProvider(handler=AuthHandler(), manager=manager)
