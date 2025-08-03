import streamlit as st
import requests

API_URL = "https://aposentai-api.onrender.com/"

st.set_page_config(page_title="AposentAI", layout="centered")

st.title("🧠 AposentAI — Simulador de Aposentadoria com IA")

idade = st.number_input("Idade atual", min_value=18, max_value=100, value=30)
aporte = st.number_input("Aporte mensal (R$)", min_value=0.0, step=100.0, value=1000.0)

if st.button("Simular"):
    with st.spinner("Calculando com IA..."):
        try:
            response = requests.post(f"{API_URL}/simulacoes/", json={
                "idade": idade,
                "aporte": aporte,
                "resultado": 99999.99  # valor fixo até criar simulação real
            })

            if response.status_code == 200:
                data = response.json()
                st.success(f"Resultado simulado: R$ {data['resultado']:.2f}")
                st.write("Explicação gerada com IA:")
                st.markdown(data["explicacao"])
            else:
                st.error("Erro na API. Verifique a entrada ou tente mais tarde.")

        except Exception as e:
            st.error(f"Erro de conexão: {str(e)}")
