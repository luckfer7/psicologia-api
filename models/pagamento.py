from decimal import Decimal
from sqlalchemy import Column, String
from database.database import Base

class Pagamento (Base):
    __tablename__ = "Pagamento"
    valor = Column(Decimal)
    forma_de_pagamento = Column(String) #aqui vai ser enum
    status_do_pagamento = Column(String) #aqui vai ser enum
