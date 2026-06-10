from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SessaoResponse(BaseModel):
    id: int
    data_horario: datetime
    status: str
    paciente_id: int