import os
import asyncio
import google.generativeai as genai

# 1. Configuração do Cérebro do JARVIS (Gemini)
# IMPORTANTE: Substitua pelo seu token gerado no Google AI Studio
GOOGLE_API_KEY = "AIzaSyANUdjj389fqx7UjpYyEPsLoIyg37M9YJA"
genai.configure(api_key=GOOGLE_API_KEY)

# Definindo como o Jarvis deve agir (Personalidade)
PROMPT_SISTEMA = (
    "Você é o JARVIS, o assistente virtual sofisticado, britânico, espirituoso "
    "e altamente eficiente de Tony Stark. Responda em português de forma polida, "
    "curta, use 'Senhor' para se referir ao usuário e seja direto."
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=PROMPT_SISTEMA
)

# Inicializa o chat com o Jarvis
chat = model.start_chat(history=[])

async def main():
    print("JARVIS: Sistema online e pronto, Senhor. Como posso ajudar?")
    
    # Exemplo simples de interação por texto enquanto estruturamos o app
    while True:
        comando = input("\nVocê: ")
        
        if "desligar" in comando.lower() or "parar" in comando.lower():
            print("JARVIS: Desligando sistemas. Até logo, Senhor.")
            break
            
        resposta = chat.send_message(comando)
        print(f"JARVIS: {resposta.text}")

if __name__ == "__main__":
    asyncio.run(main())
