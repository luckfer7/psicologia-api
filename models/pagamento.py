
from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func 
from database.database import Base

class Pagamento (Base):
    __tablename__ = "pagamentos"
    id = Column(Integer, primary_key=True, index=True)
    sessao_id = Column(
        Integer,
        ForeignKey("Sessao.id"),
        nullable=False
    )
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    valor = Column(Numeric(10, 2), nullable=False)
    forma_pagamento = Column(String(50), nullable=False) #aqui vai ser enum
    data_pagamento = Column(
            DateTime,
            nullable=False,
            server_default=func.now()
    ) #aqui vai ser enum
    observacao = Column(Text, nullable=True)
    sessao = relationship(
        "Sessao",
        back_populates="pagamentos"
    )
