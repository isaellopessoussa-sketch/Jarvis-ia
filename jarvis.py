import os
import asyncio
import webbrowser
import google.generativeai as genai
from gtts import gTTS
import pygame

# 1. Configuração do Cérebro do JARVIS (Gemini)
GOOGLE_API_KEY = "AIzaSyANUdjj389fqx7UjpYyEPsLoIyg37M9YJA" # Lembre de colocar sua chave aqui
genai.configure(api_key=GOOGLE_API_KEY)

PROMPT_SISTEMA = (
    "Você é o JARVIS, o assistente virtual sofisticado, britânico, espirituoso "
    "e altamente eficiente de Tony Stark. Responda em português de forma polida, "
    "curta, use 'Senhor' para se referir ao usuário e seja direto."
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=PROMPT_SISTEMA
)
chat = model.start_chat(history=[])

# 2. Função de Voz
def falar(texto_para_falar):
    print(f"JARVIS: {texto_para_falar}")
    tts = gTTS(text=texto_para_falar, lang='pt', slow=False)
    tts.save("jarvis_voz.mp3")
    
    pygame.mixer.init()
    pygame.mixer.music.load("jarvis_voz.mp3")
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
        
    pygame.mixer.quit()
    if os.path.exists("jarvis_voz.mp3"):
        os.remove("jarvis_voz.mp3")

# 3. Função para executar comandos no celular/PC
def executar_comando(comando_usuario):
    cmd = comando_usuario.lower()
    
    if "abrir youtube" in cmd:
        falar("Abrindo o YouTube imediatamente, Senhor.")
        webbrowser.open("https://www.youtube.com")
        return True
    elif "abrir google" in cmd:
        falar("Abrindo a ferramenta de busca do Google, Senhor.")
        webbrowser.open("https://www.google.com")
        return True
    elif "abrir meu github" in cmd or "abrir github" in cmd:
        falar("Acessando seu repositório no GitHub, Senhor.")
        webbrowser.open("https://github.com/isaellopessoussa-sketch/Jarvis-ia")
        return True
        
    return False

# 4. Loop Principal
async def main():
    pygame.init()
    falar("Sistemas atualizados. Online e pronto, Senhor.")
    
    while True:
        comando = input("\nVocê: ")
        
        if "desligar" in comando.lower() or "parar" in comando.lower():
            falar("Desligando sistemas de energia. Até logo, Senhor.")
            break
            
        # Primeiro, checa se é um comando de abrir algo
        foi_comando = executar_comando(comando)
        
        # Se não foi um comando de abrir site, deixa o Gemini responder normalmente
        if not foi_comando:
            resposta = chat.send_message(comando)
            falar(resposta.text)

if __name__ == "__main__":
    asyncio.run(main())
