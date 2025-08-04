import streamlit as st
import requests
import re
import unicodedata

API_URL = "https://aposentai-api.onrender.com"

st.set_page_config(page_title="AposentAI", layout="centered")

st.title("🧠 AposentAI — Simulador de Aposentadoria com IA")

def clean_text(text):
    text = unicodedata.normalize("NFKD", text)
    text = ''.join(c for c in text if ord(c) < 128)
    text = re.sub(r"R\s?([\d,.]+)", r"R$ \1", text)
    text = text.replace("\n", " ")
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()

idade = st.number_input("Idade atual", min_value=18, max_value=100, value=30)
idade_aposentadoria = st.number_input("Idade de aposentadoria", min_value=idade+1, max_value=100, value=65)
aporte = st.number_input("Aporte mensal (R$)", min_value=0, step=100, value=1000, format="%d")

if st.button("Simular"):
    with st.spinner("Calculando com IA..."):
        try:
            response = requests.post(f"{API_URL}/simulacoes/", json={
                "idade": idade,
                "idade_aposentadoria": idade_aposentadoria,
                "aporte": aporte,
                "resultado": 0
            })

            if response.status_code == 200:
                data = response.json()
                st.success(f"Resultado simulado: R$ {int(data['resultado']):,}".replace(",", "."))
                st.write("Explicação gerada com IA:")
                st.write(clean_text(data["explicacao"]))
            else:
                st.error(f"Erro: {response.status_code} — {response.text}")

        except Exception as e:
            st.error(f"Erro de conexão: {str(e)}")

st.markdown("---")

if st.button("📜 Ver histórico de simulações"):
    with st.spinner("Carregando histórico..."):
        try:
            r = requests.get(f"{API_URL}/simulacoes/")
            if r.status_code == 200:
                historico = r.json()
                if not historico:
                    st.info("Nenhuma simulação encontrada.")
                else:
                    for s in historico:
                        st.markdown(f"""
                        🧾 **{s['timestamp'][:10]}**
                        - Idade: {s['idade']}
                        - Aporte: R$ {int(s['aporte']):,}".replace(",", ".") + f"
                        - Resultado: R$ {int(s['resultado']):,}".replace(",", ".") + f"
                        - Explicação: {clean_text(s['explicacao'])}
                        """)
            else:
                st.error("Erro ao buscar histórico.")
        except Exception as e:
            st.error(f"Erro de conexão: {str(e)}")
