import os
import streamlit as st
from datetime import datetime
import google.generativeai as genai
from gtts import gTTS
import base64

# 1. Configuração da API Key via Secrets
try:
    GOOGLE_API_KEY = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception:
    st.error("Erro crítico: Chave 'GEMINI_KEY' ausente nos Secrets.")

ano_atual = datetime.now().year
PROMPT_SISTEMA = f"Você é o JARVIS, o assistente de Tony Stark. Responda em português, curto, use 'Senhor' e seja direto. Ano: {ano_atual}."

try:
    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-flash", 
        system_instruction=PROMPT_SISTEMA
    )
except Exception as e:
    st.error(f"Erro no modelo: {e}")

st.set_page_config(page_title="JARVIS OS", page_icon="🤖")

st.title("JARVIS")
st.write("<p style='text-align:center; color:#00E5FF;'>INTERFACE INTELIGENTE ONLINE</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if comando := st.chat_input("Diga suas diretrizes, Senhor..."):
    with st.chat_message("user"):
        st.markdown(comando)
    st.session_state.messages.append({"role": "user", "content": comando})

    contexto = "".join([f"{m['role']}: {m['content']}\n" for m in st.session_state.messages[-5:]])
    
    try:
        resposta_ia = model.generate_content(f"{contexto}\nuser: {comando}")
        resposta = resposta_ia.text
    except Exception as e:
        resposta = f"Desculpe, Senhor. Falha na diretriz. Detalhes: {e}"

    with st.chat_message("assistant"):
        st.markdown(resposta)
    st.session_state.messages.append({"role": "assistant", "content": resposta})
