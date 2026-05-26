from pydantic import BaseModel
from datetime import datetime

class AnotacaoCreate(BaseModel):
    texto: str
    sessao_id: int