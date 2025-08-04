# 🧠 AposentAI

**AposentAI** é um simulador de aposentadoria inteligente que combina cálculo financeiro real com explicações geradas por inteligência artificial. O projeto foi desenvolvido como portfólio técnico para uma vaga de Desenvolvedor Backend com Foco em IA Aplicada.

---

## ✨ Funcionalidades

- 💻 Backend com **FastAPI** e arquitetura modular
- 📊 Cálculo real de patrimônio usando **juros compostos mensais**
- 🤖 Explicações automatizadas com **Groq + LLaMA 3 (70B)**
- 💾 Banco de dados local com **SQLite** usando SQLAlchemy
- 🌐 Interface acessível via **Streamlit** (frontend online)
- 📂 Histórico completo de simulações salvas no banco
- 🐳 Pronto para **deploy com Docker** (diferencial MLOps)
- ☁️ Deploy 100% gratuito via **Render.com** e **Streamlit Cloud**

---

## 🧠 Como funciona

1. O usuário informa:
   - Idade atual
   - Idade desejada para aposentadoria
   - Valor que pretende investir por mês

2. A aplicação:
   - Calcula o patrimônio estimado ao final do período, considerando uma taxa real de 0,6% ao mês
   - Gera uma explicação automática com IA (modelo LLaMA 3) para interpretar o resultado
   - Salva a simulação no banco de dados e exibe no histórico

---

## 🔗 Acesso ao app

- **Frontend (Streamlit):** https://aposentia.streamlit.app  
- **Backend (FastAPI):** https://aposentai-api.onrender.com  

---

## 📷 Preview

> <img width="983" height="851" alt="image" src="https://github.com/user-attachments/assets/f57de5c1-6909-4787-a57e-a2863bfa1a80" />
*

---

## 📂 Estrutura do projeto

```
aposentai/
├── app/
│   ├── main.py         ← API FastAPI
│   ├── db.py           ← Conexão com SQLite
│   ├── models.py       ← Tabela Simulacao
│   ├── schemas.py      ← Pydantic (entrada da API)
├── streamlit_app.py    ← Interface Streamlit
├── requirements.txt    ← Dependências
├── Dockerfile          ← Container backend
```

---

## ⚙️ Rodando localmente

### Requisitos:
- Python 3.11+
- Docker (opcional)

### Passos:

```bash
# Clone o projeto
git clone https://github.com/SEU-USUARIO/aposentai.git
cd aposentai

# Instale dependências (modo local)
pip install -r requirements.txt

# Rode a API localmente (modo dev)
uvicorn app.main:app --reload

# Ou rode com Docker
docker build -t aposentai-api .
docker run -p 8000:8000 aposentai-api

# Rode a interface Streamlit
streamlit run streamlit_app.py
```

---

## 🔐 Variáveis de ambiente (para backend)

No ambiente de produção (ex: Render), adicione:

```
GROQ_API_KEY=sk-xxxxxx
```

---

## 🛠 Stack utilizada

| Camada       | Tecnologia                           |
|--------------|---------------------------------------|
| Backend      | FastAPI + SQLite + SQLAlchemy         |
| IA           | Groq API com LLaMA 3 (70B)            |
| Frontend     | Streamlit                             |
| Deploy API   | Render.com                            |
| Deploy Front | Streamlit Cloud                       |
| Container    | Docker (imagem leve Python 3.11)      |

---

## 👨‍💻 Autor

Desenvolvido por Nathan Jardim.

---
