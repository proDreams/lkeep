"""
Проект: Lkeep
Автор: Иван Ашихмин
Год: 2025
Специально для проекта "Код на салфетке"
https://pressanybutton.ru/category/servis-na-fastapi/
"""

import smtplib
from email.message import EmailMessage

from celery import shared_task
from starlette.templating import Jinja2Templates

from lkeep.core.settings import settings


@shared_task
def send_text_confirmation_email(to_email: str, token: str) -> None:
    """
    Отправляет текстовое подтверждение регистрации по электронной почте.

    :param to_email: Адрес электронной почты получателя подтверждения.
    :type to_email: str
    :param token: Токен для подтверждения регистрации.
    :type token: str
    """
    confirmation_url = f"{settings.frontend_url}/auth/register_confirm?token={token}"

    text = f"""Спасибо за регистрацию!
Для подтверждения регистрации перейдите по ссылке: {confirmation_url}
"""

    message = EmailMessage()
    message.set_content(text)
    message["From"] = settings.email_settings.email_username
    message["To"] = to_email
    message["Subject"] = "Подтверждение регистрации"

    with smtplib.SMTP_SSL(host=settings.email_settings.email_host, port=settings.email_settings.email_port) as smtp:
        smtp.login(
            user=settings.email_settings.email_username,
            password=settings.email_settings.email_password.get_secret_value(),
        )
        smtp.send_message(msg=message)


@shared_task
def send_confirmation_email(to_email: str, token: str) -> None:
    """
    Отправляет подтверждение регистрации по электронной почте.

    :param to_email: Адрес электронной почты получателя сообщения.
    :type to_email: str
    :param token: Токен для подтверждения регистрации, передаваемый в URL.
    :type token: str
    """
    confirmation_url = f"{settings.frontend_url}/auth/register_confirm?token={token}"

    templates = Jinja2Templates(directory=settings.templates_dir)
    template = templates.get_template(name="confirmation_email.html")
    html_content = template.render(confirmation_url=confirmation_url)

    message = EmailMessage()
    message.add_alternative(html_content, subtype="html")
    message["From"] = settings.email_settings.email_username
    message["To"] = to_email
    message["Subject"] = "Подтверждение регистрации"

    with smtplib.SMTP_SSL(host=settings.email_settings.email_host, port=settings.email_settings.email_port) as smtp:
        smtp.login(
            user=settings.email_settings.email_username,
            password=settings.email_settings.email_password.get_secret_value(),
        )
        smtp.send_message(msg=message)
