from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal, engine
from app.models import Base, Simulacao

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"msg": "API do AposentAI funcionando"}

@app.post("/simulacoes/")
def criar_simulacao(idade: int, aporte: float, resultado: float, db: Session = Depends(get_db)):
    simulacao = Simulacao(idade=idade, aporte=aporte, resultado=resultado, explicacao="simulação básica")
    db.add(simulacao)
    db.commit()
    db.refresh(simulacao)
    return simulacao
