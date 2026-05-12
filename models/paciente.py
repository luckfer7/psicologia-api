from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from database.database import Base

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    data_nascimento = Column(Date)
    telefone = Column(String)
    email = Column(String)
    observacoes = Column(String)
    status = Column(String, default="ativo")

    #é no model que se faz as relações entre as classes. Ou seja, aqui.
    #Usa-se o relationship
    sessoes = relationship("Sessao")

