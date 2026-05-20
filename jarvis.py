import os
import streamlit as st
from datetime import datetime
import google.generativeai as genai
from gtts import gTTS
import base64

# 1. Configuração do Cérebro do JARVIS (Gemini)
# COLE SUA CHAVE DO GEMINI AQUI
GOOGLE_API_KEY = "AIzaSyANUdjj389fqx7UjpYyEPsLoIyg37M9YJA" 
genai.configure(api_key=GOOGLE_API_KEY)

ano_atual = datetime.now().year

PROMPT_SISTEMA = (
    f"Você é o JARVIS, o assistente virtual sofisticado de Tony Stark. Responda em português de forma polida, "
    f"curta, use 'Senhor' para se referir ao usuário e seja direto. Ano atual: {ano_atual}."
)

model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=PROMPT_SISTEMA)

# Configuração da página do App no celular
st.set_page_config(page_title="JARVIS OS", page_icon="🤖", layout="centered")

# Estilo CSS para deixar com cara de sistema do Homem de Ferro (Neon e Escuro)
st.markdown("""
    <style>
    .stApp { background-color: #05050A; color: #FFFFFF; }
    h1 { color: #00E5FF !important; font-family: 'Courier New', monospace; text-align: center; }
    .stChatMessage { background-color: #0A0A14 !important; border: 1px solid #102A45; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("J.A.R.V.I.S.")
st.write("<p style='text-align:center; color:#00E5FF; opacity:0.7;'>INTERFACE DE REDE INTELIGENTE ONLINE</p>", unsafe_allow_html=True)

# Inicializa o histórico de conversa se não existir
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Exibe as mensagens antigas na tela com visual de chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Função para gerar áudio player escondido e falar no celular
def falar_no_navegador(texto):
    tts = gTTS(text=texto, lang='pt', slow=False)
    tts.save("jarvis_voz.mp3")
    with open("jarvis_voz.mp3", "rb") as f:
        audio_bytes = f.read()
    audio_base64 = base64.b64encode(audio_bytes).decode()
    # Cria um player de áudio HTML invisível que toca sozinho (autoplay)
    audio_html = f'<audio src="data:audio/mp3;base64,{audio_base64}" autoplay style="display:none;"></audio>'
    st.markdown(audio_html, unsafe_allow_html=True)
    os.remove("jarvis_voz.mp3")

# Barra de comando na parte de baixo da tela
if comando := st.chat_input("Diga suas diretrizes, Senhor..."):
    # Mostra o que você digitou
    with st.chat_message("user"):
        st.markdown(comando)
    st.session_state.messages.append({"role": "user", "content": comando})

    # Pede a resposta para a IA
    resposta = st.session_state.chat.send_message(comando).text

    # Mostra a resposta do JARVIS
    with st.chat_message("assistant"):
        st.markdown(resposta)
    st.session_state.messages.append({"role": "assistant", "content": resposta})
    
    # Faz o celular falar
    falar_no_navegador(resposta)
