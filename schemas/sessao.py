from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class SessaoCreate(BaseModel):
    data: date
    horario: datetime
    anotacao: str 
    paciente_id: int