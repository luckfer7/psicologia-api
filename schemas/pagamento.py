from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
from enum import Enum

class PagamentoCreate(BaseModel):
    sessao_id: int
    valor: Decimal = Field(gt=0)
    forma_pagamento: str
    observacao: Optional[str] = None

class PagamentoResponse(BaseModel):
    id: int
    sessao_id: int
    valor: Decimal
    forma_pagamento: str
    data_pagamento: datetime
    observacao: Optional[str] = None

    class Config:
        from_attributes = True

class ResumofinanceiroSessao(BaseModel):
    sessao_id: int
    valor_cobrado: Decimal
    total_pago: Decimal
    saldo_pendente: Decimal
    status: str
class Pagamento(BaseModel):
    paciente_id: int
    valor: Decimal
    forma_de_pagamento: PagamentoForma
    status_de_pagamento: PagamentoStatus

class PagamentoForma (str, Enum):
    pix = "pix"
    dinheiro = "dinheiro"
    credito = "credito"
    debito = "debito"

class PagamentoStatus (bool):
    pago = "pago"
    pendente = "pendente"