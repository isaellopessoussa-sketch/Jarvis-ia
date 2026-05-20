import os
import webbrowser
from datetime import datetime

# Conexão com o sistema Android do celular via Pydroid 3
try:
    import android
    droid = android.Android()
except ImportError:
    droid = None

ARQUIVO_MEMORIA = "jarvis_memoria.txt"

def salvar_na_memoria(informacao):
    with open(ARQUIVO_MEMORIA, "a", encoding="utf-8") as f:
        f.write(f"- {informacao}\n")

def executar_automacao_fisica(comando_usuario):
    cmd = comando_usuario.lower()
    
    # --- LANTERNA ---
    if "ligar lanterna" in cmd:
        if droid:
            droid.cameraToggleFlashlight(True)
            return "Lanterna ativada. Iluminando o ambiente, Senhor."
        return "Sensor de lanterna indisponível neste dispositivo, Senhor."
        
    elif "desligar lanterna" in cmd:
        if droid:
            droid.cameraToggleFlashlight(False)
            return "Lanterna desativada, Senhor."
        return "Sensor de lanterna indisponível neste dispositivo, Senhor."

    # --- BATERIA ---
    elif "status da bateria" in cmd or "bateria" in cmd:
        if droid:
            droid.batteryStartMonitoring()
            porcentagem = droid.batteryGetLevel().result
            droid.batteryStopMonitoring()
            return f"Os níveis de energia estão em {porcentagem}%, Senhor."
        return "Acesso aos dados de energia negado pelo sistema, Senhor."

    # --- MEMÓRIA ---
    elif "lembre que" in cmd or "guarde que" in cmd:
        fato = comando_usuario.replace("lembre que", "").replace("guarde que", "").strip()
        salvar_na_memoria(fato)
        return f"Entendido, Senhor. Arquivei em meus bancos de dados: '{fato}'."
    
    # --- APLICATIVOS ---
    elif "abrir youtube" in cmd:
        webbrowser.open("https://www.youtube.com")
        return "Abrindo o YouTube, Senhor."
    elif "abrir whatsapp" in cmd:
        webbrowser.open("whatsapp://")
        return "Iniciando o WhatsApp, Senhor."
    elif "abrir spotify" in cmd:
        webbrowser.open("spotify://")
        return "Sintonizando suas músicas no Spotify, Senhor."
        
    # Se não for nenhum comando físico, devolve False para o cérebro (Gemini) responder
    return False
