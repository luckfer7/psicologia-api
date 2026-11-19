from fastapi import FastAPI
from database.database import engine, Base, SessionLocal
from models.paciente import Paciente
from schemas.paciente import PacienteCreate
from schemas.PacienteResponse import PacienteResponse
from schemas.paciente import PacienteUpdate

from schemas.sessao import SessaoCreate
from models.sessao import Sessao
from models.pagamento import Pagamento

from schemas.pagamento import (
    PagamentoCreate,
    PagamentoResponse,
    ResumofinanceiroSessao
)

from decimal import Decimal
from sqlalchemy import func
from datetime import datetime

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

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#Aqui, cria-se as tabelas
#Base.metadata.create_all(bind=engine). Removido! Não é mais necessário

@app.get("/")
def home():
    return {"mensagem": "API rodando!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins= [
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#----------------ENDPOINTS PARA PACIENTES-------------------------------
@app.get("/pacientes", response_model=list[PacienteResponse])
def mostrar_pacientes(usuario: Usuario = Depends(get_current_user)):
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
def buscar_paciente(paciente_id: int, usuario: Usuario = Depends(get_current_user)):
    db = SessionLocal()

    paciente = db.query(Paciente).filter(
        Paciente.usuario_id == usuario.id,
        Paciente.id == paciente_id
        ).first()

    db.close()

    return paciente

#Paciente.usuario_id == usuario.id
@app.get("/pacientes/{paciente_nome}", response_model=PacienteResponse)
def buscar_paciente_pelo_nome(paciente_nome: str, usuario: Usuario = Depends(get_current_user)):
    db = SessionLocal()

    nome_do_paciente = db.query(Paciente).filter(
        Paciente.usuario_id == usuario.id,
        Paciente.nome == paciente_nome).first()

    db.close()

    return nome_do_paciente

@app.post("/adicionar_pacientes")
def criar_paciente(paciente: PacienteCreate, usuario: Usuario = Depends(get_current_user)):
    #HERDA O PACIENTECREATE E JOGA A CLASSE PRA VARIAVEL EM MINUSCULO
    db = SessionLocal()

    novo_paciente = Paciente(
        nome=paciente.nome,
        telefone=paciente.telefone,
        email=paciente.email,
        data_nascimento=paciente.data_nascimento,
        observacoes=paciente.observacoes,
        usuario_id=usuario.id,
        status=paciente.status,
        valor_sessao=paciente.valor_sessao
    )

    db.add(novo_paciente) #prepara a fila para salvar no banco
    db.commit() #Responsável por de fato executar o sql que salva no banco
    db.refresh(novo_paciente) #Responsável por sincronizar com o banco

    return novo_paciente

@app.put("/pacientes/{paciente_id}")
def atualizar_paciente(paciente_id: int, dados: PacienteUpdate, usuario: Usuario = Depends(get_current_user)):
    db = SessionLocal()

    paciente = db.query(Paciente).filter(
        Paciente.usuario_id == usuario.id,
        Paciente.id == paciente_id, 
        Paciente.usuario_id == usuario.id).first()

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
def deletar_paciente(paciente_id: int, usuario: Usuario = Depends(get_current_user)):
    db = SessionLocal()

    #Primeiro busca o paciente
    paciente = db.query(Paciente).filter(
        Paciente.usuario_id == usuario.id,
        Paciente.id == paciente_id).first()

    if not paciente:
        db.close()
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    db.delete(paciente)
    db.commit()

    db.close()

    return {"mensagem": "Paciente deletado com sucesso"}

@app.get("/pacientes/{paciente_id}/sessoes")
def sessoes_pacientes(paciente_id: int, usuario: Usuario = Depends(get_current_user)):
    db = SessionLocal()

    sessoes_do_paciente = (db.query(Sessao).join(Paciente).filter(
        Paciente.usuario_id == usuario.id,
        Sessao.paciente_id == paciente_id).all()
    )

    db.close()

    return sessoes_do_paciente
#---------------------------ENDPOINTS PARA SESSOES---------------------------------

@app.post("/criar_sessao")
def criar_sessao(sessao: SessaoCreate, usuario: Usuario = Depends(get_current_user)):
    db = SessionLocal()

    #verifica-se se o pacinete realmente pertence ao usuario logado
    paciente = (
        db.query(Paciente)
        .filter(
            Paciente.id == sessao.paciente_id,
            Paciente.usuario_id == usuario.id
        )
        .first()
    )
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    nova_sessao = Sessao(
        data_horario=sessao.data_horario,
        # anotacao=sessao.anotacao,
        #status=sessao.status,
        status=sessao.status.value,
        #paciente=sessao.paciente_id
        paciente_id=paciente.id,
        valor_cobrado=paciente.valor_sessao
    )

    db.add(nova_sessao)
    db.commit()
    db.refresh(nova_sessao)

    db.close()
    return nova_sessao

#------------------------------------------------------------------

@app.post("/anotacoes")
def criar_anotacao(anotacao: AnotacaoCreate, usuario: Usuario = Depends(get_current_user)):
    db = SessionLocal()

    sessao = (
        db.query(Sessao)
        .join(Paciente)
        .filter(
            Sessao.id == anotacao.sessao_id,
            Paciente.usuario_id == usuario.id
        )
        .first()
    )
    if not sessao:
        db.close()
        raise HTTPException(status_code=404, detail="Sessão não encontrada.")

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
@app.get("/sessoes/{sessao_id}/anotacoes")
def mostrar_anotacoes(sessao_id: int, usuario: Usuario = Depends(get_current_user)):
    db = SessionLocal()

    sessao = (
        db.query(Sessao)
        .join(Paciente)
        .filter(
            Sessao.id == sessao_id,
            Paciente.usuario_id == usuario.id
        )
        .first()
    )
    if not sessao:
        db.close()
        raise HTTPException(status_code=404, detail="Sessão não encontrada.")

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

#---------------------------ENDPOINTS PARA FINANCEIRO---------------------------------

@app.post("/pagamentos", response_model=PagamentoResponse)
def registrar_pagamento(
    dados: PagamentoCreate,
    db: Sessao = Depends(get_db),
    usuario = Depends(get_current_user)
):
    sessao = db.query(Sessao).join(Paciente).filter(
        Sessao.id == dados.sessao_id,
        Paciente.usuario_id == usuario.id
    ).first()

    if not sessao:
        raise HTTPException(
            status_code=404,
            detail="Sessão não encontrada"
        )

    if sessao.status != "realizada":
        raise HTTPException(
            status_code=400,
            detail="Só é possível registrar pagamentos de sessões realizada"
        )

    total_pago = db.query(
        func.coalesce(func.sum(Pagamento.valor), 0)
    ).filter(
        Pagamento.sessao_id == sessao.id
    ).scalar()

    saldo = Decimal(str(sessao.valor_cobrado)) - Decimal(str(total_pago))

    if dados.valor > saldo:
        raise HTTPException(
            status_code=400,
            detail="O pagamento não pode ser maior que o saldo pendente"
        )

    pagamento = Pagamento(
        sessao_id=sessao.id,
        valor=dados.valor,
        forma_pagamento=dados.forma_pagamento,
        observacao=dados.observacao
    )

    db.add(pagamento)
    db.commit()
    db.refresh(pagamento)

    return pagamento

@app.get("/sessoes/{sessao_id}/pagamentos", response_model=list[PagamentoResponse])
def listar_pagamentos_sessao(
    sessao_id: int,
    db: Sessao = Depends(get_db),
    usuario = Depends(get_current_user)
):
    sessao = db.query(Sessao).join(Paciente).filter(
        Sessao.id == sessao_id,
        Paciente.usuario_id == usuario.id
    ).first()

    if not sessao:
        raise HTTPException(
            status_code=404,
            detail="Sessão não encontrada"
        )

    return db.query(Pagamento).filter(
        Pagamento.sessao_id == sessao_id
    ).order_by(Pagamento.data_pagamento.desc()).all()

@app.get("/financeiro/pendentes")
def listar_sessoes_pendentes(
    db: Sessao = Depends(get_db),
    usuario = Depends(get_current_user)
):
    sessoes = db.query(Sessao).join(Paciente).filter(
        Paciente.usuario_id == usuario.id,
        Sessao.status == "realizada"
    ).all()

    resultado = []

    for sessao in sessoes:
        total_pago = db.query(
            func.coalesce(func.sum(Pagamento.valor), 0)
        ).filter(
            Pagamento.sessao_id == sessao.id
        ).scalar()

        valor = Decimal(str(sessao.valor_cobrado or 0))
        recebido = Decimal(str(total_pago or 0))
        saldo = valor - recebido

        if saldo > 0:
            resultado.append({
                "sessao_id": sessao.id,
                "paciente_id": sessao.paciente_id,
                "paciente_nome": sessao.paciente.nome,
                "data_horario": sessao.data_horario,
                "valor_cobrado": valor,
                "total_pago": recebido,
                "saldo_pendente": saldo,
                "status_financeiro": (
                    "parcial" if recebido > 0 else "pendente"
                )
            })
        return resultado

@app.get("/financeiro/resumo")
def resumo_financeiro(
    db: Sessao = Depends(get_db),
    usuario = Depends(get_current_user)
):
    agora = datetime.now()

    inicio_mes = agora.replace(
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    pagamentos = db.query(Pagamento).join(
        Sessao
    ).join(
        Paciente
    ).filter(
        Paciente.usuario_id == usuario.id,
        Pagamento.data_pagamento >= inicio_mes
    ).all()

    recebido_mes = sum(
        (Decimal(str(p.valor)) for p in pagamentos),
        Decimal("0.00")
    )

    sessoes_pendentes = listar_sessoes_pendentes(
        db=db,
        usuario=usuario
    )

    total_pendente = sum(
        (
            item["saldo_pendente"]
            for item in sessoes_pendentes
        ),
        Decimal("0.00")
    )

    return {
        "recebido_mes": recebido_mes,
        "total_pendente": total_pendente,
        "quantidade_pendentes": len(sessoes_pendentes)
    }

@app.get("/financeiro/historico")
def historico_pagamentos(
    db: Sessao = Depends(get_db),
    usuario = Depends(get_current_user)
): 
    pagamentos = db.query(Pagamento).join(
        Sessao
    ).join(
        Paciente
    ).filter(
        Paciente.usuario_id == usuario.id
    ).order_by(
        Pagamento.data_pagamento.desc()
    ).all()

    return [
        {
            "id": p.id,
            "sessao_id": p.sessao_id,
            "paciente": p.sessao.paciente.nome,
            "valor": p.valor,
            "forma_pagamento": p.forma_pagamento,
            "data_pagamento": p.data_pagamento
        }
        for p in pagamentos
    ]