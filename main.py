from fastapi import FastAPI
from database.database import engine, Base, SessionLocal
from models.paciente import Paciente
from schemas.paciente import PacienteCreate
from schemas.PacienteResponse import PacienteResponse
from schemas.paciente import PacienteUpdate

from schemas.sessao import SessaoCreate
from models.sessao import Sessao

from schemas.anotacao import AnotacaoCreate
from models.anotacao import Anotacao


from models.usuario import Usuario
from schemas.usuario import UsuarioCreate
from utils.seguranca import gerar_hash

from schemas.login import LoginRequest
from utils.jwt import criar_token
from utils.seguranca import verificar_senha

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from utils.autenticacao import get_current_user

from fastapi import HTTPException

from sqlalchemy.orm import joinedload

app = FastAPI()

#Aqui, cria-se as tabelas
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"mensagem": "API rodando!"}

#----------------ENDPOINTS PARA PACIENTES-------------------------------
@app.get("/pacientes", response_model=list[PacienteResponse])
def mostrar_pacientes(usuario=Depends(get_current_user)):
    db = SessionLocal()

    pacientes = (
        db.query(Paciente)
        .filter(Paciente.usuario_id == usuario.id)
        .options(joinedload(Paciente.sessoes))
        .all()
    ) #Por baixo dos panos, é tipo SELECT *FROM pacientes LEFT JOIN sessoes
    db.close()
    return pacientes

@app.get("/pacientes/{paciente_id}", response_model=PacienteResponse)
def buscar_paciente(paciente_id: int):
    db = SessionLocal()

    paciente = db.query(Paciente).filter(
        Paciente.id == paciente_id
        ).first()

    db.close()

    return paciente

#Paciente.usuario_id == usuario.id
@app.get("/pacientes/{paciente_nome}", response_model=PacienteResponse)
def buscar_paciente_pelo_nome(paciente_nome: str):
    db = SessionLocal()

    nome_do_paciente = db.query(Paciente).filter(Paciente.nome == paciente_nome).first()

    db.close()

    return nome_do_paciente

@app.post("/adicionar_pacientes")
def criar_paciente(paciente: PacienteCreate):
    #HERDA O PACIENTECREATE E JOGA A CLASSE PRA VARIAVEL EM MINUSCULO
    db = SessionLocal()

    novo_paciente = Paciente(
        nome=paciente.nome,
        telefone=paciente.telefone,
        email=paciente.email,
        data_nascimento=paciente.data_nascimento,
        observacoes=paciente.observacoes,
        # usuario_id=usuario.id
    )

    db.add(novo_paciente) #prepara a fila para salvar no banco
    db.commit() #Responsável por de fato executar o sql que salva no banco
    db.refresh(novo_paciente) #Responsável por sincronizar com o banco

    return novo_paciente

@app.put("/pacientes/{paciente_id}")
def atualizar_paciente(paciente_id: int, dados: PacienteUpdate):
    db = SessionLocal()

    paciente = db.query(Paciente).filter(Paciente.id == paciente_id, Paciente.usuario_id == usuario.id).first()

    if not paciente:
        db.close()
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        #só pega os campos que vieram no JSON

        setattr(paciente, campo, valor)
        #atualiza dinamicamente
    

    db.commit()
    db.refresh(paciente)

    db.close()

    return paciente

@app.delete("/pacientes/{paciente_id}")
def deletar_paciente(paciente_id: int):
    db = SessionLocal()

    #Primeiro busca o paciente
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()

    if not paciente:
        db.close()
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    db.delete(paciente)
    db.commit()

    db.close()

    return {"mensagem": "Paciente deletado com sucesso"}

@app.get("/pacientes/{paciente_id}/sessoes")
def sessoes_pacientes(paciente_id: int):
    db = SessionLocal()

    sessoes_do_paciente = db.query(Sessao).filter(Sessao.paciente_id == paciente_id).all()

    db.close()

    return sessoes_do_paciente
#---------------------------ENDPOINTS PARA SESSOES---------------------------------

@app.post("/criar_sessao")
def criar_sessao(sessao: SessaoCreate):
    db = SessionLocal()

    nova_sessao = Sessao(
        data_horario=sessao.data_horario,
        # anotacao=sessao.anotacao,
        #status=sessao.status,
        status=sessao.status.value,
        #paciente=sessao.paciente_id
        paciente_id=sessao.paciente_id

    )

    db.add(nova_sessao)
    db.commit()
    db.refresh(nova_sessao)

    return nova_sessao

#------------------------------------------------------------------

@app.post("/anotacoes")
def criar_anotacao(anotacao: AnotacaoCreate):
    db = SessionLocal()

    nova_anotacao = Anotacao(
        texto=anotacao.texto,
        sessao_id=anotacao.sessao_id
    )

    db.add(nova_anotacao)

    db.commit()

    db.refresh(nova_anotacao)

    db.close()

    return nova_anotacao

#Aqui se busca a anotação por sessao
@app.get("/sessoes/{id}/anotacoes")
def mostrar_anotacoes(sessao_id: int):
    db = SessionLocal()

    anotacao = db.query(Anotacao).filter(Anotacao.sessao_id == sessao_id).all()

    db.close()

    return anotacao

#Endpoint de autenticação
@app.post("/auth/register")
def registrar_usuario(usuario: UsuarioCreate):
    db = SessionLocal()

    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=gerar_hash(usuario.senha)
    )

    db.add(novo_usuario)

    db.commit()

    db.refresh(novo_usuario)

    db.close()

    return {
        "mensagem": "Usuário criado com sucesso"
    }

#Endpoint de login
@app.post("/auth/login")
def login(dados: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()

    usuario = (
        db.query(Usuario)
        .filter(Usuario.email == dados.username)
        .first()
    )

    if not usuario:
        db.close()

        raise HTTPException(
            status_code=401,
            detail="Email ou senha inválido."
        )
    
    senha_valida = verificar_senha(
        dados.password,
        usuario.senha_hash
    )

    if not senha_valida:
        db.close()

        raise HTTPException(
            status_code=401,
            detail="Email ou senha inválidos."
        )
    
    token = criar_token(
        {
            "sub": str(usuario.id)
        }
    )

    db.close()

    return {
        "access_token": token,
        "token_type": "bearer"
    }