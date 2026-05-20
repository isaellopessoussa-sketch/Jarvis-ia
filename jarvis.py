import os
import webbrowser
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
import google.generativeai as genai
from gtts import gTTS
import pygame
import requests

# --- COMPATIBILIDADE COM CELULAR (ANDROID) ---
try:
    import android
    droid = android.Android()
except ImportError:
    droid = None

# 1. Configuração do Cérebro do JARVIS (Gemini)
GOOGLE_API_KEY = "AIzaSyANUdjj389fqx7UjpYyEPsLoIyg37M9YJA" # Cole sua chave aqui
genai.configure

ARQUIVO_MEMORIA = "jarvis_memoria.txt"
ano_atual = datetime.now().year

def ler_memoria_permanente():
    if os.path.exists(ARQUIVO_MEMORIA):
        with open(ARQUIVO_MEMORIA, "r", encoding="utf-8") as f:
            return f.read()
    return "Nenhum dado prévio salvo sobre o Usuário."

def salvar_na_memoria(informacao):
    with open(ARQUIVO_MEMORIA, "a", encoding="utf-8") as f:
        f.write(f"- {informacao}\n")

memorias_recuperadas = ler_memoria_permanente()

PROMPT_SISTEMA = (
    f"Você é o JARVIS, o assistente virtual sofisticado, britânico, espirituoso "
    f"e altamente eficiente de Tony Stark. Responda em português de forma polida, "
    f"curta, use 'Senhor' para se referir ao usuário e seja direto.\n"
    f"CONTEXTO TEMPORAL: Estamos no ano de {ano_atual}.\n"
    f"MEMÓRIA DE LONGO PRAZO DO USUÁRIO:\n{memorias_recuperadas}"
)

model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=PROMPT_SISTEMA)
chat = model.start_chat(history=[])

pygame.init()

# 2. Função de Voz Integrada com a Tela
def falar(texto_para_falar):
    painel_texto.insert(tk.END, f"JARVIS: {texto_para_falar}\n\n")
    painel_texto.see(tk.END) 
    root.update() 
    
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

# 3. Ferramentas de Automação e Agente Integradas
def executar_automacao_e_agente(comando_usuario):
    cmd = comando_usuario.lower()
    
    # --- MÓDULO AGENTE AUTÔNOMO ---
    if "missão" in cmd or "execute" in cmd or "autônomo" in cmd:
        falar("Ativando protocolos autônomos. Processando dados, Senhor...")
        try:
            # O Jarvis pesquisa o clima de forma autônoma na web para criar um relatório
            resposta_web = requests.get("https://wttr.in/?format=%C++%t", timeout=5)
            dados = resposta_web.text.strip() if resposta_web.status_code == 200 else "Sistemas offline"
            
            relatorio = f"RELATÓRIO AUTÔNOMO DO JARVIS:\nMissão baseada no comando: {comando_usuario}\nSensores climáticos indicam: {dados}.\nAnálise concluída com sucesso, Senhor."
            
            with open("missao_jarvis.txt", "w", encoding="utf-8") as f:
                f.write(relatorio)
                
            falar("Missão cumprida de forma autônoma, Senhor. Relatório gerado e salvo em 'missao_jarvis.txt'.")
        except:
            falar("Falha ao executar a tarefa autônoma, Senhor.")
        return True

    # --- MÓDULO HARDWARE (LANTERNA) ---
    elif "ligar lanterna" in cmd:
        if droid:
            droid.cameraToggleFlashlight(True)
            falar("Lanterna ativada. Iluminando o ambiente, Senhor.")
        else:
            falar("Sensor de lanterna não detectado no computador, Senhor.")
        return True
        
    elif "desligar lanterna" in cmd:
        if droid:
            droid.cameraToggleFlashlight(False)
            falar("Lanterna desativada, Senhor.")
        else:
            falar("Sensor de lanterna indisponível, Senhor.")
        return True

    # --- MÓDULO HARDWARE (BATERIA) ---
    elif "status da bateria" in cmd or "bateria" in cmd:
        if droid:
            droid.batteryStartMonitoring()
            porcentagem = droid.batteryGetLevel().result
            droid.batteryStopMonitoring()
            falar(f"Os níveis de energia celular estão em {porcentagem}%, Senhor.")
        else:
            falar("Monitoramento de bateria disponível apenas no dispositivo móvel, Senhor.")
        return True

    # --- MÓDULO MEMÓRIA ---
    elif "lembre que" in cmd or "guarde que" in cmd:
        fato = comando_usuario.replace("lembre que", "").replace("guarde que", "").strip()
        salvar_na_memoria(fato)
        falar(f"Entendido, Senhor. Arquivei em meus bancos de dados: '{fato}'.")
        return True
    
    # --- MÓDULO APLICATIVOS ---
    elif "abrir youtube" in cmd:
        falar("Abrindo o YouTube, Senhor.", text_output, page)
        webbrowser.open("https://www.youtube.com")
        return True
    elif "abrir whatsapp" in cmd:
        falar("Iniciando o WhatsApp, Senhor.", text_output, page)
        webbrowser.open("whatsapp://")
        return True
    elif "abrir spotify" in cmd:
        falar("Sintonizando suas músicas no Spotify, Senhor.", text_output, page)
        webbrowser.open("spotify://")
        return True
        
    return False

# 4. Ação do Botão Enviar
def enviar_comando():
    comando = campo_entrada.get()
    if not comando:
        return
        
    campo_entrada.delete(0, tk.END)
    painel_texto.insert(tk.END, f"Você: {comando}\n")
    
    # Executa primeiro os comandos locais unificados
    foi_resolvido = executar_automacao_e_agente(comando)
    
    # Se não for comando local, joga para a IA conversar normal
    if not foi_resolvido:
        resposta = chat.send_message(comando)
        falar(resposta.text)

# --- 5. INTERFACE VISUAL TKINTER (Tudo em um só arquivo!) ---
root = tk.Tk()
root.title("JARVIS - All-in-One OS")
root.configure(bg="#05050A")
root.geometry("400x600")

lbl_titulo = tk.Label(root, text="J.A.R.V.I.S.", font=("Courier", 26, "bold"), fg="#00E5FF", bg="#05050A")
lbl_titulo.pack(pady=10)

lbl_status = tk.Label(root, text="⚡ ARMAÇÃO TOTALMENTE INTEGRADA", font=("Courier", 9), fg="#00E5FF", bg="#05050A")
lbl_status.pack()

painel_texto = scrolledtext.ScrolledText(root, width=42, height=22, font=("Courier", 11), bg="#0A0A14", fg="#FFFFFF", insertbackground="#00E5FF", bd=0, highlightthickness=1, highlightbackground="#102A45")
painel_texto.pack(pady=15, padx=15)

campo_entrada = tk.Entry(root, width=28, font=("Courier", 14), bg="#0A0A14", fg="#00E5FF", insertbackground="#00E5FF", bd=0, highlightthickness=1, highlightbackground="#00E5FF")
campo_entrada.pack(pady=5)
campo_entrada.bind("<Return>", lambda event: enviar_comando())

btn_enviar = tk.Button(root, text="TRANSMITIR", font=("Courier", 11, "bold"), bg="#00E5FF", fg="#05050A", activebackground="#FFFFFF", command=enviar_comando, bd=0, padx=25, pady=6)
btn_enviar.pack(pady=10)

root.after(1000, lambda: falar("Módulos de automação, agência e interface unificados. Sistema totalmente estável, Senhor."))

root.mainloop()
