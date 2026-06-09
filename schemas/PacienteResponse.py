from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from schemas.SessaoResponse import SessaoResponse
class PacienteResponse(BaseModel):
    id: int
    nome: str
    telefone: Optional [str]
    email: Optional [str]
    data_nascimento: Optional [date]
    observacoes: Optional [str]
    sessoes: List[SessaoResponse]
    class Config:
        from_attributes = True #Sem isso, o FastAPI não consegue converter o objeto do banco em JSON.
