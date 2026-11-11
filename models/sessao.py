#data, horario, assunto abordado / anotações
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Numeric
from database.database import Base

class Sessao (Base):
    __tablename__ = "Sessao"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    data_horario = Column(DateTime)
    # anotacao = Column(String)
    status = Column(String)
    valor_cobrado = Column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )
    pagamentos = relationship(
        "Pagamento",
        back_populates="sessao",
        cascade="all, delete-orphan"
    )