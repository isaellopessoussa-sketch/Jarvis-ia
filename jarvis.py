import os
import streamlit as st
from datetime import datetime
import google.generativeai as genai
from gtts import gTTS
import base64

# 1. Configuração do Cérebro do JARVIS (Gemini)
GOOGLE_API_KEY "AIzaSyC_J-L1-f0do3qK2-YvI12lCwbRIGsNdy0" 
genai.configure(api_key=GOOGLE_API_KEY)

ano_atual = datetime.now().year

PROMPT_SISTEMA = (
    f"Você é o JARVIS, o assistente virtual sofisticado de Tony Stark. Responda em português de forma polida, "
    f"curta, use 'Senhor' para se referir ao usuário e seja direto. Ano atual: {ano_atual}."
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", 
    system_instruction=PROMPT_SISTEMA
)

# Configuração da página do App
st.set_page_config(page_title="JARVIS OS", page_icon="🤖", layout="centered")

# Estilo visual futurista
st.markdown("""
    <style>
    .stApp { background-color: #05050A; color: #FFFFFF; }
    h1 { color: #00E5FF !important; font-family: 'Courier New', monospace; text-align: center; }
    .stChatMessage { background-color: #0A0A14 !important; border: 1px solid #102A45; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("J.A.R.V.I.S.")
st.write("<p style='text-align:center; color:#00E5FF; opacity:0.7;'>INTERFACE DE REDE INTELIGENTE ONLINE</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def falar_no_navegador(texto):
    try:
        tts = gTTS(text=texto, lang='pt', slow=False)
        tts.save("jarvis_voz.mp3")
        with open("jarvis_voz.mp3", "rb") as f:
            audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        audio_html = f'<audio src="data:audio/mp3;base64,{audio_base64}" autoplay style="display:none;"></audio>'
        st.markdown(audio_html, unsafe_allow_html=True)
        os.remove("jarvis_voz.mp3")
    except:
        pass

if comando := st.chat_input("Diga suas diretrizes, Senhor..."):
    with st.chat_message("user"):
        st.markdown(comando)
    st.session_state.messages.append({"role": "user", "content": comando})

    contexto_conversa = ""
    for msg in st.session_state.messages[-5:]:
        contexto_conversa += f"{msg['role']}: {msg['content']}\n"
    
    prompt_final = f"{contexto_conversa}\nuser: {comando}"

    try:
        resposta_ia = model.generate_content(prompt_final)
        resposta = resposta_ia.text
    except Exception as e:
        resposta = "Desculpe, Senhor. Meus sistemas de comunicação com o servidor falharam. Verifique se a API Key está correta."

    with st.chat_message("assistant"):
        st.markdown(resposta)
    st.session_state.messages.append({"role": "assistant", "content": resposta})
    
    falar_no_navegador(resposta)
