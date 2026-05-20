import os
import datetime
import google.generativeai as genai
import flet as ft

# 1. Configuração da API Key (O Flet puxa das variáveis de ambiente do sistema)
CHAVE_API_DO_GOOGLE = os.getenv("GEMINI_KEY")
if not CHAVE_API_DO_GOOGLE:
    # Se você testar localmente e não tiver a variável, coloque sua chave aqui para testar:
    CHAVE_API_DO_GOOGLE = "SUA_CHAVE_GEMINI_AQUI"

genai.configure(chave_api=CHAVE_API_DO_GOOGLE)

ano_real = datetime.datetime.now().year
PROMPT_SISTEMA = f"Você é o JARVIS, o assistente de Tony Stark. Responda em português."

try:
    modelo = genai.GenerativeModel(
        model_name="models/gemini-1.5-flash",
        system_instruction=PROMPT_SISTEMA
    )
except Exception as e:
    print(f"Erro no modelo: {e}")

def main(page: ft.Page):
    page.title = "JARVIS OS"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.END

    # Histórico do chat para o Flet e para o Gemini
    chat_historico = ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS)
    conversa_gemini = modelo.start_chat(history=[])

    def enviar_mensagem(e):
        if not campo_texto.value:
            return
        
        # Mensagem do Usuário
        user_msg = campo_texto.value
        chat_historico.controls.append(
            ft.Text(f"Senhor: {user_msg}", color=ft.colors.BLUE_200, size=16)
        )
        campo_texto.value = ""
        page.update()

        # Resposta do Jarvis
        try:
            resposta = conversa_gemini.send_message(user_msg)
            chat_historico.controls.append(
                ft.Text(f"JARVIS: {resposta.text}", color=ft.colors.CYAN_ACCENT, size=16)
            )
        except Exception as err:
            chat_historico.controls.append(
                ft.Text(f"JARVIS: Erro ao processar... {err}", color=ft.colors.RED_400)
            )
        
        page.update()

    # Elementos da Tela
    campo_texto = ft.TextField(
        hint_text="Diga suas diretrizes, Senhor...",
        expand=True,
        on_submit=enviar_mensagem
    )
    botao_enviar = ft.IconButton(
        icon=ft.icons.SEND,
        icon_color=ft.colors.CYAN_ACCENT,
        on_click=enviar_mensagem
    )

    # Layout da página
    page.add(
        ft.Container(
            content=chat_historico,
            expand=True,
            padding=20
        ),
        ft.Row(
            controls=[campo_texto, botao_enviar],
            padding=10
        )
    )

# Importante para o Flet saber que vai rodar como app
if __name__ == "__main__":
    ft.app(target=main)
