from fastapi import FastAPI
from database.database import engine, Base, SessionLocal
from models.paciente import Paciente

app = FastAPI()

#Aqui, cria-se as tabelas
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"mensagem": "API rodando!"}


@app.get("/pacientes")
def mostrar_pacientes():
    db = SessionLocal()

    pacientes = db.query(Paciente).all() #Por baixo dos panos, é tipo SELCT FROM na tabela

    return pacientes

@app.post("/adicionar_pacientes")
def criar_paciente():
    db = SessionLocal()

    novo_paciente = Paciente(
        nome="Teste",
        telefone="21994468609"
    )

    db.add(novo_paciente) #prepara a fila para salvar no banco
    db.commit() #Responsável por de fato executar o sql que salva no banco
    db.refresh(novo_paciente) #Responsável por sincronizar com o banco

    return novo_paciente