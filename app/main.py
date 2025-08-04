from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.db import SessionLocal, engine
from app.models import Base, Simulacao
from app.schemas import SimulacaoRequest
from openai import OpenAI
import os

Base.metadata.create_all(bind=engine)
app = FastAPI()

# Liberar acesso do frontend Streamlit
origins = [
    "https://aposentia.streamlit.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conectar à API da Groq
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# Conexão com o banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Cálculo de patrimônio futuro com juros compostos
def calcular_patrimonio_futuro(idade: int, idade_aposentadoria: int, aporte: float) -> float:
    meses = (idade_aposentadoria - idade) * 12
    taxa_mensal = 0.006

    if meses <= 0:
        return 0.0

    montante = aporte * (((1 + taxa_mensal) ** meses - 1) / taxa_mensal)
    return round(montante, 2)

# Geração da explicação com IA
def gerar_explicacao_com_ia(idade: int, aporte: float, resultado: float, idade_aposentadoria: int) -> str:
    prompt = (
        f"Explique de forma direta o seguinte caso: uma pessoa de {idade} anos contribui com "
        f"R$ {aporte:,.2f} por mês até os {idade_aposentadoria} anos. No final, o montante acumulado foi "
        f"de R$ {resultado:,.2f}. Responda como se estivesse explicando em uma entrevista de emprego, de forma clara, concisa e em no máximo 5 linhas."
    )

    resposta = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    return resposta.choices[0].message.content.strip()

# Teste da API
@app.get("/")
def read_root():
    return {"msg": "API do AposentAI funcionando"}

# Criar nova simulação
@app.post("/simulacoes/")
def criar_simulacao(request: SimulacaoRequest, db: Session = Depends(get_db)):
    resultado = calcular_patrimonio_futuro(request.idade, request.idade_aposentadoria, request.aporte)
    explicacao = gerar_explicacao_com_ia(request.idade, request.aporte, resultado, request.idade_aposentadoria)

    simulacao = Simulacao(
        idade=request.idade,
        aporte=request.aporte,
        resultado=resultado,
        explicacao=explicacao
    )
    db.add(simulacao)
    db.commit()
    db.refresh(simulacao)
    return simulacao

# Listar todas as simulações
@app.get("/simulacoes/")
def listar_simulacoes(db: Session = Depends(get_db)):
    return db.query(Simulacao).order_by(Simulacao.timestamp.desc()).all()
