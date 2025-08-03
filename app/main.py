from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal, engine
from app.models import Base, Simulacao
from openai import OpenAI
import os

Base.metadata.create_all(bind=engine)
app = FastAPI()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def gerar_explicacao_com_ia(idade: int, aporte: float, resultado: float) -> str:
    prompt = (
        f"Explique de forma simples o seguinte cenário: uma pessoa com {idade} anos "
        f"planeja investir R$ {aporte:,.2f} por mês até se aposentar. O valor final simulado "
        f"foi de R$ {resultado:,.2f}. Use linguagem acessível e objetiva."
    )

    resposta = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return resposta.choices[0].message.content.strip()

@app.post("/simulacoes/")
def criar_simulacao(idade: int, aporte: float, resultado: float, db: Session = Depends(get_db)):
    explicacao = gerar_explicacao_com_ia(idade, aporte, resultado)
    simulacao = Simulacao(idade=idade, aporte=aporte, resultado=resultado, explicacao=explicacao)
    db.add(simulacao)
    db.commit()
    db.refresh(simulacao)
    return simulacao

@app.get("/")
def read_root():
    return {"msg": "API do AposentAI funcionando"}