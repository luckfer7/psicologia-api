
from sqlalchemy import Column, String, Integer, ForeignKey, Numeric
from database.database import Base

class Pagamento (Base):
    __tablename__ = "Pagamento"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    valor = Column(Numeric(10, 2))
    forma_de_pagamento = Column(String) #aqui vai ser enum
    status_de_pagamento = Column(String) #aqui vai ser enum
