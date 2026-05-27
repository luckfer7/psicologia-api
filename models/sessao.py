#data, horario, assunto abordado / anotações

from sqlalchemy import Column, Date, String, Integer, DateTime, ForeignKey
from database.database import Base

class Sessao (Base):
    __tablename__ = "Sessao"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    data_horario = Column(DateTime)
    # anotacao = Column(String)
    status = Column(String)