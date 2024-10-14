import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv('.env'))


class DBSettings:
    MODE: str = os.environ.get('MODE')
    DB_HOST: str = os.environ.get('DB_HOST')
    DB_PORT: str = os.environ.get('DB_PORT')
    DB_USER: str = os.environ.get('DB_USER')
    DB_PASS: str = os.environ.get('DB_PASS')
    DB_NAME: str = os.environ.get('DB_NAME')

    DB_URL: str = (
        f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    )


class EmailSettings:
    MAIL_FROM: str = os.environ.get('MAIL_FROM')
    MAIL_USERNAME: str = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD: str = os.environ.get('MAIL_PASSWORD')
    MAIL_HOST: str = os.environ.get('MAIL_HOST')
    MAIL_PORT: str = os.environ.get('MAIL_PORT')


db_settings = DBSettings()
email = EmailSettings()
