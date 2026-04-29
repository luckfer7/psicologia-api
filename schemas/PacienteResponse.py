from pydantic import BaseModel
from datetime import date

class PacienteResponse(BaseModel):
    nome: str
    telefone: str
    observacoes: str
