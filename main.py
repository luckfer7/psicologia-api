from fastapi import FastAPI
from database.database import engine, Base, SessionLocal
from models.paciente import Paciente
from schemas.paciente import PacienteCreate
from schemas.PacienteResponse import PacienteResponse

app = FastAPI()

#Aqui, cria-se as tabelas
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"mensagem": "API rodando!"}


@app.get("/pacientes")
def mostrar_pacientes(paciente: PacienteResponse):
    db = SessionLocal()

    pacientes = db.query(paciente(
        nome=paciente.nome,
        telefone=paciente.telefone,
        observacoes=paciente.observacoes
    )).all() #Por baixo dos panos, é tipo SELECT FROM na tabela

    return pacientes

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