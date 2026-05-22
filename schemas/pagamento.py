from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
from enum import Enum

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