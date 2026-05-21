from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from enum import Enum

class Pagamento(BaseModel):
    paciente_id: int
    