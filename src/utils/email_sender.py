import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import APIRouter

from src.core.config import email
from src.schemas.company import MailBody

company_router = APIRouter()


def send_email(msg: MailBody) -> dict:
    message = MIMEMultipart('alternative')
    message['From'] = email.MAIL_FROM
    message['To'] = msg.to
    message['Subject'] = msg.subject

    part = MIMEText(msg.body, 'html')
    message.attach(part)

    try:
        server = smtplib.SMTP(email.MAIL_HOST, email.MAIL_PORT)
        server.esmtp_features['auth'] = 'LOGIN PLAIN'
        server.login(email.MAIL_USERNAME, email.MAIL_PASSWORD)
        server.sendmail(email.MAIL_FROM, msg.to, message.as_string())
    except smtplib.SMTPRecipientsRefused as smtp_error:
        return {'status': f'Failed to send email. Invalid recipient: {msg.to}'}
