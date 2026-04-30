from pydantic import BaseModel
from typing import Optional
from datetime import date

class PacienteResponse(BaseModel):
    id: int
    nome: str
    telefone: Optional [str]
    email: Optional [str]
    data_nascimento: Optional [date]
    observacoes: Optional [str]

    class Config:
        from_attributes = True #Sem isso, o FastAPI não consegue converter o objeto do banco em JSON.
