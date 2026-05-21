import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import google.generativeai as genai

# Configura a chave do Gemini que você salvou no GitHub Secrets
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", ""))

class JarvisChat(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Título do App
        self.add_widget(Label(text="JARVIS IA", size_hint_y=0.05, font_size='20sp', bold=True))

        # Área de conversa com rolagem
        self.scroll = ScrollView(size_hint_y=0.75)
        self.chat_logs = Label(
            text="Jarvis: Olá! Como posso te ajudar hoje?\n",
            alignment=('left', 'top'),
            size_hint_y=None,
            valign='top',
            halign='left'
        )
        self.chat_logs.bind(size=self.ajustar_texto)
        self.scroll.add_widget(self.chat_logs)
        self.add_widget(self.scroll)

        # Barra inferior (Campo de texto + Botão)
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=5)
        
        self.txt_input = TextInput(hint_text="Digite sua mensagem...", multiline=False)
        self.txt_input.bind(on_text_validate=self.enviar_mensagem) # Envia ao apertar "Enter"
        
        btn_enviar = Button(text="Enviar", size_hint_x=0.25, background_color=(0, 0.5, 1, 1))
        btn_enviar.bind(on_release=self.enviar_mensagem)

        input_layout.add_widget(self.txt_input)
        input_layout.add_widget(btn_enviar)
        self.add_widget(input_layout)

    def ajustar_texto(self, instance, value):
        # Faz o texto quebrar a linha certinho e rolar para baixo
        self.chat_logs.text_size = (instance.width, None)
        self.chat_logs.height = self.chat_logs.texture_size[1]

    def enviar_mensagem(self, instance):
        user_text = self.txt_input.text.strip()
        if not user_text:
            return

        # Mostra o que o usuário digitou
        self.chat_logs.text += f"\nVocê: {user_text}\n"
        self.txt_input.text = ""

        try:
            # Chama a inteligência artificial do Gemini
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(user_text)
            jarvis_response = response.text
        except Exception as e:
            jarvis_response = "Erro ao conectar com o Jarvis. Verifique sua chave API."

        # Mostra a resposta do Jarvis
        self.chat_logs.text += f"Jarvis: {jarvis_response}\n"

class JarvisApp(App):
    def build(self):
        return JarvisChat()

if __name__ == '__main__':
    JarvisApp().run()
