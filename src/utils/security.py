import bcrypt
import jwt
from fastapi import Header, HTTPException, status

from src.schemas.auth import AuthJwt

auth_jwt_config = AuthJwt()


def encode_jwt(
        payload: dict,
        private_key: str = auth_jwt_config.private_key.read_text(),
        algorithm: str = auth_jwt_config.algorithm,
) -> str:
    encoded = jwt.encode(payload, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
        token: str,
        public_key: str = auth_jwt_config.public_key.read_text(),
        algorithm: str = auth_jwt_config.algorithm,
) -> dict:
    try:
        decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    else:
        return decoded


def hash_password(
        password: str,
) -> str:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt).decode()


def validate_password(
        password: str,
        hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )


def validate_auth_user(
        authorization: str = Header(...),
) -> str:
    if not authorization.startswith('Bearer '):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authorization header format',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    token = authorization[len('Bearer '):]  # Извлекаем сам токен
    try:
        # Декодируем JWT и получаем payload
        payload = decode_jwt(token)
        email = payload.get('email')
        if email is None:
            raise HTTPException(  # noqa: TRY301
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid token: email not found',
                headers={'WWW-Authenticate': 'Bearer'},
            )

    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    else:
        return email


def validate_email_from_token(email_from_token: str, curr_email: str) -> None:
    if email_from_token != curr_email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Email from token does not match with the provided email',
        )
