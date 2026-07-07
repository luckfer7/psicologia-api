from fastapi.security import OAuth2PasswordBearer

from jose import jwt
from jose import JWTError

from fastapi import Depends, HTTPException
from database.database import SessionLocal
from models.usuario import Usuario

from utils.jwt import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)
#Esse trecho de código diz ao fastapi que as rotas protegidas recebem um Bearer Token

def verificar_token(token: str):
    try:
        payload = jwt.decode(
            token, 
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload
    
    except JWTError:

        return None
    
def get_current_user(
        token: str = Depends(oauth2_scheme)
):
    payload = verificar_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="token inválido"
        )
    
    usuario_id = payload.get("sub")

    db = SessionLocal()

    usuario = (
        db.query(Usuario)
        .filter(Usuario.id == int(usuario_id))
        .first()
    )

    db.close()

    if usuario is None:

        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado"
        )
    
    return usuario
    #Essa função pega o bearer token, decodifica, procura o usuario no banco e devolve o objeto usuário.
