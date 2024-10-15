import bcrypt
import jwt
from fastapi import HTTPException, status

from src.schemas.auth import AuthJwt

auth_jwt_config = AuthJwt()


def encode_jwt(
        payload: AdminJwtPayload,
        private_key: str = auth_jwt_config.private_key.read_text(),
        algorithm: str = auth_jwt_config.algorithm,
) -> str:
    payload = payload.__dict__
    encoded = jwt.encode(payload, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
        token: str,
        public_key: str = auth_jwt_config.public_key.read_text(),
        algorithm: str = auth_jwt_config.algorithm,
) -> str:
    try:
        decoded = jwt.decode(token, public_key, algorithm=[algorithm])
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
