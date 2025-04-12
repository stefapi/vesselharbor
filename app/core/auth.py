import os
import datetime
from dotenv import load_dotenv
from authlib.jose import jwt, JoseError

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

def create_access_token(data: dict, expires_delta: datetime.timedelta = None, token_type: str = "access") -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "token_type": token_type})
    token = jwt.encode({"alg": ALGORITHM}, to_encode, SECRET_KEY)
    # Authlib peut renvoyer des bytes ; on convertit en str si nécessaire
    return token.decode("utf-8") if isinstance(token, bytes) else token

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY)
        payload.validate()
        return payload
    except JoseError:
        raise Exception("Token invalide ou expiré")
