from pathlib import Path

from pydantic import BaseModel

BASE_DIR = Path(__file__).parent.parent


class AuthJwt(BaseModel):
    private_key: Path = BASE_DIR / 'auth_keys' / 'private.pem'
    public_key: Path = BASE_DIR / 'auth_keys' / 'public.pem'
    algorithm: str = 'RS256'
