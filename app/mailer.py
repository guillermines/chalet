from .config import settings
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER="./templates/email",
)


def send_email_background(
    background_tasks: BackgroundTasks, subject: str, email_to: str, body: dict
):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype="html",
    )
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message, template_name="email.html")
