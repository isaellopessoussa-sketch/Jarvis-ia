import os
import asyncio
import webbrowser
from datetime import datetime
import google.generativeai as genai
from gtts import gTTS
import pygame
import flet as ft

# LINK COM OS OUTROS ARQUIVOS: Importa seus novos módulos automaticamente
try:
    import automacao
    import agente
except ImportError:
    automacao = None
    agente = None

# 1. Configuração do Cérebro do JARVIS (Gemini)
# COLQUE SUA API KEY AQUI TAMBÉM
GOOGLE_API_KEY = "import os
import asyncio
import webbrowser
from datetime import datetime
import google.generativeai as genai
from gtts import gTTS
import pygame
import flet as ft

# LINK COM OS OUTROS ARQUIVOS: Importa seus novos módulos automaticamente
try:
    import automacao
    import agente
except ImportError:
    automacao = None
    agente = None

# 1. Configuração do Cérebro do JARVIS (Gemini)
# COLQUE SUA API KEY AQUI TAMBÉM
GOOGLE_API_KEY = "AIzaSyANUdjj389fqx7UjpYyEPsLoIyg37M9YJA" 
genai.configure(api_key=GOOGLE_API_KEY)

ARQUIVO_MEMORIA = "jarvis_memoria.txt"

def ler_memoria_permanente():
    if os.path.exists(ARQUIVO_MEMORIA):
        with open(ARQUIVO_MEMORIA, "r", encoding="utf-8") as f:
            return f.read()
    return "Nenhum dado prévio salvo sobre o Usuário."

memorias_recuperadas = ler_memoria_permanente()
ano_atual = datetime.now().year

PROMPT_SISTEMA = (
    f"Você é o JARVIS, o assistente virtual sofisticado, britânico, espirituoso "
    f"e altamente eficiente de Tony Stark. Responda em português de forma polida, "
    f"curta, use 'Senhor' para se referir ao usuário e seja direto.\n"
    f"CONTEXTO TEMPORAL: Estamos no ano de {ano_atual}.\n"
    f"MEMÓRIA DE LONGO PRAZO DO USUÁRIO:\n{memorias_recuperadas}"
)

model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=PROMPT_SISTEMA)
chat = model.start_chat(history=[])

# 2. Função de Voz
def falar(texto_para_falar, text_output_widget=None, page=None):
    if text_output_widget and page:
        text_output_widget.value = f"JARVIS: {texto_para_falar}"
        page.update()
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

# 3. Central de Comando Inteligente
def processar_comando_geral(comando_usuario, text_output, page):
    cmd = comando_usuario.lower()
    
    # SE FOR UMA MISSÃO AUTÔNOMA (Ex: "jarvis, execute a missão...")
    if "missão" in cmd or "execute" in cmd or "autônomo" in cmd:
        if agente:
            falar("Ativando protocolos autônomos. Aguarde um instante, Senhor.", text_output, page)
            resultado_missao = agente.executar_missao_autonoma(comando_usuario)
            falar(resultado_missao, text_output, page)
            return True
        else:
            falar("Módulo de autonomia (agente.py) não foi encontrado, Senhor.", text_output, page)
            return True

    # SE FOR UM COMANDO FÍSICO DO CELULAR (Lanterna, Bateria, Abrir Apps)
    if automacao:
        resultado_fisico = automacao.executar_automacao_fisica(comando_usuario)
        if resultado_fisico: # Se o automacao.py reconheceu o comando
            falar(resultado_fisico, text_output, page)
            return True
            
    return False

# 4. Interface Gráfica (Flet)
def main(page: ft.Page):
    page.title = "JARVIS - Main Core OS"
    page.background_color = "#0B0F19"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    pygame.init()

    titulo = ft.Text("J.A.R.V.I.S.", size=32, color="#00E5FF", weight=ft.FontWeight.BOLD, font_family="monospace")
    subtitulo = ft.Text("SISTEMA TOTALMENTE INTEGRADO", size=12, color="#00E5FF", opacity=0.6)
    output_texto = ft.Text("Aguardando diretrizes, Senhor...", size=16, color="#FFFFFF", text_align=ft.TextAlign.CENTER, width=300)
    
    campo_comando = ft.TextField(
        label="Comando para o sistema...",
        label_style=ft.TextStyle(color="#00E5FF"),
        border_color="#00E5FF",
        color="#FFFFFF",
        width=300,
        text_align=ft.TextAlign.CENTER
    )

    reator_arc = ft.Container(
        content=ft.Icon(ft.Icons.VALENTINES_ROUNDED, color="#00E5FF", size=50),
        alignment=ft.alignment.center,
        width=120,
        height=120,
        shape=ft.BoxShape.CIRCLE,
        border=ft.border.all(3, "#00E5FF"),
        bgcolor="#102A45"
    )

    def enviar_click(e):
        comando = campo_comando.value
        if not comando:
            return
        campo_comando.value = ""
        output_texto.value = f"Você: {comando}"
        page.update()
        
        # Tenta rodar os módulos locais primeiro (Automação ou Agente)
        foi_resolvido = processar_comando_geral(comando, output_texto, page)
        
        # Se nenhum módulo local resolveu, joga para o Chat normal do Gemini
        if not foi_resolvido:
            resposta = chat.send_message(comando)
            falar(resposta.text, output_texto, page)

    botao_enviar = ft.ElevatedButton(text="TRANSMITIR", color="#0B0F19", bgcolor="#00E5FF", width=150, on_click=enviar_click)

    page.add(titulo, subtitulo, ft.Divider(height=20, color="transparent"), reator_arc, ft.Divider(height=30, color="transparent"), output_texto, ft.Divider(height=20, color="transparent"), campo_comando, botao_enviar)
    falar("Todos os módulos foram unificados com sucesso. Sistema 100% operacional, Senhor.", output_texto, page)

ft.app(target=main)" 
genai.configure(api_key=GOOGLE_API_KEY)

ARQUIVO_MEMORIA = "jarvis_memoria.txt"

def ler_memoria_permanente():
    if os.path.exists(ARQUIVO_MEMORIA):
        with open(ARQUIVO_MEMORIA, "r", encoding="utf-8") as f:
            return f.read()
    return "Nenhum dado prévio salvo sobre o Usuário."

memorias_recuperadas = ler_memoria_permanente()
ano_atual = datetime.now().year

PROMPT_SISTEMA = (
    f"Você é o JARVIS, o assistente virtual sofisticado, britânico, espirituoso "
    f"e altamente eficiente de Tony Stark. Responda em português de forma polida, "
    f"curta, use 'Senhor' para se referir ao usuário e seja direto.\n"
    f"CONTEXTO TEMPORAL: Estamos no ano de {ano_atual}.\n"
    f"MEMÓRIA DE LONGO PRAZO DO USUÁRIO:\n{memorias_recuperadas}"
)

model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=PROMPT_SISTEMA)
chat = model.start_chat(history=[])

# 2. Função de Voz
def falar(texto_para_falar, text_output_widget=None, page=None):
    if text_output_widget and page:
        text_output_widget.value = f"JARVIS: {texto_para_falar}"
        page.update()
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

# 3. Central de Comando Inteligente
def processar_comando_geral(comando_usuario, text_output, page):
    cmd = comando_usuario.lower()
    
    # SE FOR UMA MISSÃO AUTÔNOMA (Ex: "jarvis, execute a missão...")
    if "missão" in cmd or "execute" in cmd or "autônomo" in cmd:
        if agente:
            falar("Ativando protocolos autônomos. Aguarde um instante, Senhor.", text_output, page)
            resultado_missao = agente.executar_missao_autonoma(comando_usuario)
            falar(resultado_missao, text_output, page)
            return True
        else:
            falar("Módulo de autonomia (agente.py) não foi encontrado, Senhor.", text_output, page)
            return True

    # SE FOR UM COMANDO FÍSICO DO CELULAR (Lanterna, Bateria, Abrir Apps)
    if automacao:
        resultado_fisico = automacao.executar_automacao_fisica(comando_usuario)
        if resultado_fisico: # Se o automacao.py reconheceu o comando
            falar(resultado_fisico, text_output, page)
            return True
            
    return False

# 4. Interface Gráfica (Flet)
def main(page: ft.Page):
    page.title = "JARVIS - Main Core OS"
    page.background_color = "#0B0F19"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    pygame.init()

    titulo = ft.Text("J.A.R.V.I.S.", size=32, color="#00E5FF", weight=ft.FontWeight.BOLD, font_family="monospace")
    subtitulo = ft.Text("SISTEMA TOTALMENTE INTEGRADO", size=12, color="#00E5FF", opacity=0.6)
    output_texto = ft.Text("Aguardando diretrizes, Senhor...", size=16, color="#FFFFFF", text_align=ft.TextAlign.CENTER, width=300)
    
    campo_comando = ft.TextField(
        label="Comando para o sistema...",
        label_style=ft.TextStyle(color="#00E5FF"),
        border_color="#00E5FF",
        color="#FFFFFF",
        width=300,
        text_align=ft.TextAlign.CENTER
    )

    reator_arc = ft.Container(
        content=ft.Icon(ft.Icons.VALENTINES_ROUNDED, color="#00E5FF", size=50),
        alignment=ft.alignment.center,
        width=120,
        height=120,
        shape=ft.BoxShape.CIRCLE,
        border=ft.border.all(3, "#00E5FF"),
        bgcolor="#102A45"
    )

    def enviar_click(e):
        comando = campo_comando.value
        if not comando:
            return
        campo_comando.value = ""
        output_texto.value = f"Você: {comando}"
        page.update()
        
        # Tenta rodar os módulos locais primeiro (Automação ou Agente)
        foi_resolvido = processar_comando_geral(comando, output_texto, page)
        
        # Se nenhum módulo local resolveu, joga para o Chat normal do Gemini
        if not foi_resolvido:
            resposta = chat.send_message(comando)
            falar(resposta.text, output_texto, page)

    botao_enviar = ft.ElevatedButton(text="TRANSMITIR", color="#0B0F19", bgcolor="#00E5FF", width=150, on_click=enviar_click)

    page.add(titulo, subtitulo, ft.Divider(height=20, color="transparent"), reator_arc, ft.Divider(height=30, color="transparent"), output_texto, ft.Divider(height=20, color="transparent"), campo_comando, botao_enviar)
    falar("Todos os módulos foram unificados com sucesso. Sistema 100% operacional, Senhor.", output_texto, page)

ft.app(target=main)
