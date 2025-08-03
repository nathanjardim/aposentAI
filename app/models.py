from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Simulacao(Base):
    __tablename__ = "simulacoes"

    id = Column(Integer, primary_key=True, index=True)
    idade = Column(Integer)
    aporte = Column(Float)
    resultado = Column(Float)
    explicacao = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
