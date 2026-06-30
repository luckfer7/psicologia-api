from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "uma-chave-bem-grande-e-secreta"

ALGORITHM = "HS256"

ACESS_TOKEN_EXPIRE_MINUTES = 60

def criar_token(dados: dict):
    dados_token = dados.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACESS_TOKEN_EXPIRE_MINUTES
    )

    dados_token.update({"exp": expire})

    token = jwt.encode(
        dados_token,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token