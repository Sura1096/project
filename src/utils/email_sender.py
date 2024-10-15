from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib
from fastapi import APIRouter

from src.core.config import email
from src.schemas.company import MailBody

company_router = APIRouter()


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
