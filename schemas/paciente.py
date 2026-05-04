from pydantic import BaseModel
from typing import Optional
from datetime import date

class PacienteCreate(BaseModel):
    nome: str
    telefone: Optional[str] = None
    email: Optional[str] = None
    data_nascimento: Optional[date] = None
    observacoes: Optional[str] = None

    # AQUI DEFINE-SE COMO O CLIENTE VAI MANDAR OS DADOS. SE FALTAR ALGO, GERA UM ERRO AUTOMÁTICO

class PacienteUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    data_nascimento: Optional[date] = None
    observacoes: Optional[str] = None
