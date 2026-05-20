import os
import asyncio
import google.generativeai as genai
from gtts import gTTS
import pygame

# 1. Configuração do Cérebro do JARVIS (Gemini)
# Coloque a sua chave do Google AI Studio entre as aspas abaixo:
GOOGLE_API_KEY = "AIzaSyANUdjj389fqx7UjpYyEPsLoIyg37M9YJA"
genai.configure(api_key=GOOGLE_API_KEY)

# Definindo a personalidade do Jarvis
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

# 2. Função para o JARVIS falar usando os alto-falantes do celular
def falar(texto_para_falar):
    print(f"JARVIS: {texto_para_falar}")
    
    # Gera o arquivo de áudio da voz em português
    tts = gTTS(text=texto_para_falar, lang='pt', slow=False)
    tts.save("jarvis_voz.mp3")
    
    # Inicializa o player e toca o áudio no celular
    pygame.mixer.init()
    pygame.mixer.music.load("jarvis_voz.mp3")
    pygame.mixer.music.play()
    
    # Espera o áudio terminar de tocar antes de continuar
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
        
    pygame.mixer.quit()
    # Apaga o arquivo temporário para não encher a memória
    if os.path.exists("jarvis_voz.mp3"):
        os.remove("jarvis_voz.mp3")

# 3. Loop Principal do Assistente
async def main():
    # Inicializa o pygame para evitar bugs de áudio
    pygame.init()
    
    falar("Sistemas online e pronto, Senhor. Como posso ajudar?")
    
    while True:
        # No celular, digitamos o comando no teclado
        comando = input("\nVocê: ")
        
        if "desligar" in comando.lower() or "parar" in comando.lower():
            falar("Desligando sistemas de energia. Até logo, Senhor.")
            break
            
        # Envia a mensagem para a IA e recebe a resposta
        resposta = chat.send_message(comando)
        
        # O Jarvis fala a resposta em voz alta
        falar(resposta.text)

if __name__ == "__main__":
    asyncio.run(main())
