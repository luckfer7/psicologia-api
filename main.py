from fastapi import FastAPI
from database.database import engine, Base
from models.paciente import Paciente

app = FastAPI()

#Aqui, cria-se as tabelas
Base.metadata.create_all(bind=engine)

@app.get("/")
def home(): 
    return {"mensagem": "API rodando!"}