from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from database.database import Base

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id")
    )

    nome = Column(String, nullable=False)
    data_nascimento = Column(Date)
    telefone = Column(String)
    email = Column(String)
    observacoes = Column(String)
    status = Column(String, default="ativo")
    valor_sessao = Column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )

    #é no model que se faz as relações entre as classes. Ou seja, aqui.
    #Usa-se o relationship
    sessoes = relationship("Sessao")

