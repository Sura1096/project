from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib
from fastapi import BackgroundTasks

from src.core.config import email
from src.schemas.company import MailBody
from src.schemas.user import UpdateEmail, UserEmail
from src.utils.security import decode_jwt, encode_jwt


async def send_email(msg: MailBody) -> dict:
    message = MIMEMultipart('alternative')
    message['From'] = email.MAIL_FROM
    message['To'] = msg.to.email
    message['Subject'] = msg.subject

    part = MIMEText(msg.body, 'html')
    message.attach(part)

    try:
        server = aiosmtplib.SMTP(email.MAIL_HOST, email.MAIL_PORT)
        await server.connect()
        await server.login(msg.to.username, msg.to.password)
        await server.sendmail(sender=email.MAIL_FROM, recipients=msg.to.email, message=message.as_string())
    except aiosmtplib.SMTPRecipientsRefused as smtp_error:
        return {'status': f'Failed to send email. Invalid recipient: {msg.to}'}


def send_token_to_admin(account: UserEmail, tasks: BackgroundTasks) -> None:
    payload = {'sub': 'admin', 'email': account.email}
    token = encode_jwt(payload)
    data = {
        'to': account,
        'subject': 'Token',
        'body': token,
    }
    tasks.add_task(send_email, MailBody(**data))


def send_token_to_user(account: UserEmail, tasks: BackgroundTasks) -> None:
    payload = {'sub': 'user', 'email': account.email}
    token = encode_jwt(payload)
    data = {
        'to': account,
        'subject': 'Token',
        'body': token,
    }
    tasks.add_task(send_email, MailBody(**data))


def send_token(invite_token: str, new_account: UpdateEmail, tasks: BackgroundTasks) -> None:
    payload = decode_jwt(invite_token)
    new_account = UserEmail(email=new_account.new_account, username=new_account.username, password=new_account.password)
    if payload.get('sub') == 'admin':
        tasks.add_task(send_token_to_admin, new_account, tasks)
    elif payload.get('sub') == 'user':
        tasks.add_task(send_token_to_user, new_account, tasks)
