import os
import requests
import google.generativeai as genai

# 1. Configuração do Cérebro do Agente
GOOGLE_API_KEY = "AIzaSyC_J-L1-f0do3qK2-YvI12lCwbRIGsNdy0"
genai.configure(api_key=GOOGLE_API_KEY)

# O prompt do Agente ensina ele a quebrar missões complexas em passos menores
PROMPT_AGENTE = (
    "Você é o módulo de Execução Autônoma do JARVIS.\n"
    "Sua missão é receber uma tarefa complexa do usuário, dividi-la em passos lógicos e executar.\n"
    "Você tem acesso a ferramentas de busca e criação de arquivos.\n"
    "Seja extremamente eficiente, focado e reporte o progresso de cada passo usando 'Senhor'."
)

model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=PROMPT_AGENTE)

# 2. Ferramentas que o Jarvis Autônomo pode usar sozinho
def ferramenta_pesquisa_internet(termo):
    """O Jarvis usa isso para buscar informações atualizadas de forma autônoma."""
    try:
        # Usa o wttr.in ou outra API simples para simular busca/dados externos básicos
        resposta = requests.get(f"https://wttr.in/{termo}?format=%C+%t", timeout=5)
        return resposta.text
    except:
        return "Falha ao conectar aos servidores de busca."

def ferramenta_criar_relatorio(nome_arquivo, conteudo):
    """O Jarvis usa isso para salvar relatórios ou resumos gerados por ele."""
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(conteudo)
    return f"Arquivo '{nome_arquivo}' criado com sucesso no sistema."

# 3. Motor de Execução Autônoma
def executar_missao_autonoma(missao_complexa):
    print(f"\n[JARVIS AGENTE]: Iniciando execução autônoma...")
    print(f"[JARVIS AGENTE]: Missão recebida: '{missao_complexa}'")
    
    # O Gemini analisa a missão e decide quais passos tomar
    prompt_analise = (
        f"Analise esta missão: '{missao_complexa}'.\n"
        "Me diga o que você precisa fazer primeiro. Responda apenas com:\n"
        "PESQUISAR: [termo] ou SALVAR: [nome_do_arquivo] ou RESPONDER: [resposta_final]"
    )
    
    resposta_ia = model.generate_content(prompt_analise).text.strip()
    
    # PASSO 1: Tomada de decisão autônoma
    if "PESQUISAR:" in resposta_ia:
        termo = resposta_ia.replace("PESQUISAR:", "").strip()
        print(f"[JARVIS AGENTE]: Decidi pesquisar dados sobre '{termo}' de forma autônoma...")
        dados = ferramenta_pesquisa_internet(termo)
        
        # PASSO 2: Processar o resultado e gerar o relatório
        print(f"[JARVIS AGENTE]: Dados coletados. Renderizando relatório final, Senhor...")
        relatorio = model.generate_content(f"Com base nesses dados: {dados}, resolva a missão: {missao_complexa}").text
        
        # PASSO 3: Salvar o resultado sozinho
        status_salvamento = ferramenta_criar_relatorio("missao_jarvis.txt", relatorio)
        return f"Missão cumprida, Senhor. {status_salvamento} O resultado foi arquivado."
        
    else:
        # Se for uma missão simples, ele resolve direto
        resposta_direta = model.generate_content(missao_complexa).text
        return resposta_direta

# Teste rápido do modo autônomo (pode ser disparado pelo arquivo principal)
if __name__ == "__main__":
    # Exemplo de missão que ele executa, pesquisa e salva sozinho
    resultado = executar_missao_autonoma("Verifique o clima de Londres e salve um relatório em texto")
    print(f"\nJARVIS: {resultado}")
