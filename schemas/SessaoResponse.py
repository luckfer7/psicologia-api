from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class SessaoResponse(BaseModel):
    id: int
    data_horario: datetime
    status: str
    paciente_id: int
    valor_cobrado: Decimal