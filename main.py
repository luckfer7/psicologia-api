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

from fastapi import HTTPException

app = FastAPI()

#Aqui, cria-se as tabelas
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"mensagem": "API rodando!"}


@app.get("/pacientes", response_model=list[PacienteResponse])
def mostrar_pacientes():
    db = SessionLocal()

    pacientes = db.query(Paciente).all() #Por baixo dos panos, é tipo SELECT FROM na tabela
    db.close()
    return pacientes

@app.get("/pacientes/{paciente_id}", response_model=PacienteResponse)
def buscar_paciente(paciente_id: int):
    db = SessionLocal()

    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()

    db.close()

    return paciente

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
        observacoes=paciente.observacoes
    )

    db.add(novo_paciente) #prepara a fila para salvar no banco
    db.commit() #Responsável por de fato executar o sql que salva no banco
    db.refresh(novo_paciente) #Responsável por sincronizar com o banco

    return novo_paciente

@app.put("/pacientes/{paciente_id}")
def atualizar_paciente(paciente_id: int, dados: PacienteUpdate):
    db = SessionLocal()

    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()

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

#--------------------------------------------------------------------------------------------------------------------------

@app.post("/criar_sessao")
def criar_sessao(sessao: SessaoCreate):
    db = SessionLocal()

    nova_sessao = Sessao(
        data_horario=sessao.data_horario,
        anotacao=sessao.anotacao,
        status=sessao.status,
        paciente=sessao.paciente_id

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