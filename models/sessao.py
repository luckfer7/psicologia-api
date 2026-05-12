#data, horario, assunto abordado / anotações

from sqlalchemy import Column, Date, String, Integer, DateTime, ForeignKey
from database.database import Base

class Sessao (Base):
    __tablename__ = "sessao"

    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    data = Column(Date)
    horario = Column(DateTime)
    anotacao = Column(String)