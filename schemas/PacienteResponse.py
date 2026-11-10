from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from decimal import Decimal
from schemas.SessaoResponse import SessaoResponse
class PacienteResponse(BaseModel):
    id: int
    nome: str
    telefone: Optional [str]
    email: Optional [str]
    data_nascimento: Optional [date]
    observacoes: Optional [str]
    sessoes: List[SessaoResponse]
    valor_sessao: Decimal
    class Config:
        from_attributes = True #Sem isso, o FastAPI não consegue converter o objeto do banco em JSON.
