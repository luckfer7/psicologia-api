from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from enum import Enum

class SessaoCreate(BaseModel):
    data_horario: datetime
    anotacao: str 
    paciente_id: int
    status: StatusSessao

class StatusSessao(str, Enum):
    agendada = "agendada"
    realizada = "realizada"
    cancelada = "cancelada"
    faltou = "faltou"