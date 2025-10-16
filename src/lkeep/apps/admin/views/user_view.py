from typing import Any

from email_validator import EmailSyntaxError, validate_email
from passlib.context import CryptContext
from starlette.requests import Request
from starlette_admin import PasswordField
from starlette_admin.contrib.sqla import ModelView
from starlette_admin.exceptions import FormValidationError

from lkeep.database.models import User


class UserView(ModelView):
    fields = [
        "id",
        "email",
        PasswordField(
            name="password",
            label="Password",
            required=True,
            exclude_from_list=True,
            exclude_from_detail=True,
            exclude_from_edit=True,
        ),
        "is_active",
        "is_verified",
        "is_superuser",
        "created_at",
        "updated_at",
    ]

    exclude_fields_from_edit = ["created_at", "updated_at"]
    exclude_fields_from_create = ["created_at", "updated_at"]

    sortable_fields = ["email", "created_at"]
    fields_default_sort = [("created_at", True)]
    searchable_fields = ["email"]

    page_size = 20
    page_size_options = [5, 10, 25, 50, -1]

    async def before_create(self, request: Request, data: dict[str, Any], user: User) -> None:
        try:
            validate_email(data["email"])
        except EmailSyntaxError:
            raise FormValidationError(errors={"email": "Invalid email"})

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        user.hashed_password = pwd_context.hash(data.pop("password"))
