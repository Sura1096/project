from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib
from fastapi import BackgroundTasks

from src.core.config import email
from src.schemas.company import MailBody
from src.utils.security import encode_jwt


async def send_email(msg: MailBody) -> dict:
    message = MIMEMultipart('alternative')
    message['From'] = email.MAIL_FROM
    message['To'] = msg.to
    message['Subject'] = msg.subject

    part = MIMEText(msg.body, 'html')
    message.attach(part)

    try:
        server = aiosmtplib.SMTP(email.MAIL_HOST, email.MAIL_PORT)
        await server.connect()
        await server.login(email.MAIL_USERNAME, email.MAIL_PASSWORD)
        await server.sendmail(email.MAIL_FROM, msg.to, message.as_string())
    except aiosmtplib.SMTPRecipientsRefused as smtp_error:
        return {'status': f'Failed to send email. Invalid recipient: {msg.to}'}


def send_token_to_admin(account: str, tasks: BackgroundTasks) -> None:
    payload = {'sub': 'admin', 'email': account}
    token = encode_jwt(payload)
    data = {
        'to': account,
        'subject': 'Token',
        'body': token,
    }
    tasks.add_task(send_email, MailBody(**data))


def send_token_to_user(account: str, tasks: BackgroundTasks) -> None:
    payload = {'sub': 'user', 'email': account}
    token = encode_jwt(payload)
    data = {
        'to': account,
        'subject': 'Token',
        'body': token,
    }
    tasks.add_task(send_email, MailBody(**data))
