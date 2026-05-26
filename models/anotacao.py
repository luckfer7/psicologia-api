from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database.database import Base
from datetime import datetime

class Anotacao(Base):
    __tablename__ = "anotacoes"
    id = Column(Integer, primary_key=True, index=True)
    texto = Column(String)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    sessao_id = Column(Integer, ForeignKey("Sessao.id"))