import os
import webbrowser
from datetime import datetime
import google.generativeai as genai
from gtts import gTTS
import pygame
import requests

# Interface do App
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

try:
    import android
    droid = android.Android()
except ImportError:
    droid = None

# Configuração da IA (COLE SUA CHAVE AQUI)
GOOGLE_API_KEY = "COLE_SUA_CHAVE_AQUI"
genai.configure(api_key=GOOGLE_API_KEY)

ARQUIVO_MEMORIA = "jarvis_memoria.txt"
ano_atual = datetime.now().year

def ler_memoria_permanente():
    if os.path.exists(ARQUIVO_MEMORIA):
        with open(ARQUIVO_MEMORIA, "r", encoding="utf-8") as f:
            return f.read()
    return "Nenhum dado prévio."

def salvar_na_memoria(informacao):
    with open(ARQUIVO_MEMORIA, "a", encoding="utf-8") as f:
        f.write(f"- {informacao}\n")

PROMPT_SISTEMA = f"Você é o JARVIS. Responda em português, curto, use 'Senhor'. Ano: {ano_atual}."
model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=PROMPT_SISTEMA)
chat = model.start_chat(history=[])

pygame.init()

class JarvisInterface(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        
        # Cor de fundo escura
        Window.clearcolor = (0.02, 0.02, 0.04, 1)

        # Título
        self.add_widget(Label(text="J.A.R.V.I.S.", font_size='28sp', bold=True, color=(0, 0.9, 1, 1), size_hint_y=None, height=40))
        self.add_widget(Label(text="SISTEMA MOBILE ONLINE", font_size='12sp', color=(0, 0.9, 1, 0.6), size_hint_y=None, height=20))

        # Histórico de Conversa
        self.scroll = ScrollView(size_hint=(1, 0.7))
        self.painel_texto = Label(text="JARVIS: Sistema iniciado, Senhor.\n\n", font_size='14sp', color=(1, 1, 1, 1), size_hint_y=None, halign='left', valign='top')
        self.painel_texto.bind(texture_size=self.painel_texto.setter('size'))
        self.scroll.add_widget(self.painel_texto)
        self.add_widget(self.scroll)

        # Entrada de Texto
        self.campo_entrada = TextInput(hint_text="Comando para o sistema...", multiline=False, size_hint_y=None, height=50, background_color=(0.04, 0.04, 0.08, 1), foreground_color=(0, 0.9, 1, 1), cursor_color=(0, 0.9, 1, 1))
        self.campo_entrada.bind(on_text_validate=self.enviar_comando)
        self.add_widget(self.campo_entrada)

        # Botão
        btn = Button(text="TRANSMITIR", size_hint_y=None, height=50, background_color=(0, 0.7, 0.9, 1), color=(0.02, 0.02, 0.04, 1), bold=True)
        btn.bind(on_press=self.enviar_comando)
        self.add_widget(btn)

    def falar(self, texto):
        self.painel_texto.text += f"JARVIS: {texto}\n\n"
        tts = gTTS(text=texto, lang='pt', slow=False)
        tts.save("jarvis_voz.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load("jarvis_voz.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()
        if os.path.exists("jarvis_voz.mp3"):
            os.remove("jarvis_voz.mp3")

    def executar_comandos(self, comando):
        cmd = comando.lower()
        if "lanterna" in cmd and droid:
            if "ligar" in cmd:
                droid.cameraToggleFlashlight(True)
                self.falar("Lanterna ativada, Senhor.")
            else:
                droid.cameraToggleFlashlight(False)
                self.falar("Lanterna desativada, Senhor.")
            return True
        elif "bateria" in cmd and droid:
            droid.batteryStartMonitoring()
            porcentagem = droid.batteryGetLevel().result
            droid.batteryStopMonitoring()
            self.falar(f"Energia em {porcentagem}%, Senhor.")
            return True
        elif "abrir youtube" in cmd:
            webbrowser.open("https://www.youtube.com")
            self.falar("Abrindo o YouTube, Senhor.")
            return True
        return False

    def enviar_comando(self, instance):
        comando = self.campo_entrada.text
        if not comando: return
        self.campo_entrada.text = ""
        self.painel_texto.text += f"Você: {comando}\n"
        
        if not self.executar_comandos(comando):
            resposta = chat.send_message(comando)
            self.falar(resposta.text)

class JarvisApp(App):
    def build(self):
        return JarvisInterface()

if __name__ == '__main__':
    JarvisApp().run()
