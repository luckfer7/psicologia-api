from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def gerar_hash(senha: str):
    print(senha)
    print(type(senha))
    return pwd_context.hash(senha)

def verificar_senha(senha: str, hash_salvo: str):
    return pwd_context.verify(
        senha,
        hash_salvo
    )