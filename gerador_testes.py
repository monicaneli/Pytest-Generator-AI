import os
import json
from dotenv import load_dotenv
from pathlib import Path
from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate

env_path = Path(__file__).resolve(strict=True).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Configurações do Azure OpenAI
# Carregar as variáveis de ambiente do arquivo .env
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

def testar_conexao_azure_openai():
    """
    Testa a conexão com a Azure OpenAI usando as credenciais do ambiente.
    """
    try:
        llm = AzureChatOpenAI(
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        )

        resposta = llm.invoke("Diga olá!")
        print(resposta.content)

        print("Conexão bem-sucedida! Resposta do modelo:", resposta)
        return True
    except Exception as e:
        print("Falha na conexão com Azure OpenAI:", e)
        return False

def gerar_testes(caminho_codigo: str, caminho_teste: str):
    """
    Gera um arquivo de testes pytest a partir de um arquivo de código Python usando LangChain e Azure OpenAI.
    A saída esperada é um JSON com: success (bool), filename (str), code (str).
    """
    with open(caminho_codigo, "r", encoding="utf-8") as f:
        codigo = f.read()

    prompt = PromptTemplate(
        input_variables=["codigo"],
        template=(
            "A partir do código Python abaixo, gere um arquivo de testes pytest. "
            "A resposta deve ser um JSON com os campos: 'success' (boolean), 'filename' (nome do arquivo de teste, ex: test_codigo.py), 'code' (conteúdo do arquivo de teste).\n"
            "O arquivo de teste deve começar com 'import pytest' e conter funções 'def test_*' para casos de sucesso e falha.\n"
            "Se não for possível gerar o teste, retorne success como false e uma mensagem explicativa em 'code'.\n"
            "Código:\n{codigo}\n"
        ),
    )

    # Configurar cliente LLM (LangChain wrapper)
    llm = AzureChatOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_version=AZURE_OPENAI_API_VERSION,
        azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME,
        temperature=0.3,
    )

    # Executar o prompt
    resposta = llm.invoke(prompt.format(codigo=codigo))

    try:
        resposta_json = json.loads(resposta.content)
    except Exception as e:
        print("Erro ao decodificar JSON:", e)
        print("Resposta recebida:\n", resposta.content)
        return

    if resposta_json.get("success") and "code" in resposta_json:
        nome_arquivo = resposta_json.get("filename") or caminho_teste
        # Prioriza o caminho informado pelo usuário
        if caminho_teste:
            nome_arquivo = caminho_teste
        pasta_destino = os.path.dirname(nome_arquivo)
        if pasta_destino and not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino, exist_ok=True)
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(resposta_json["code"])
        print(f"✅ Arquivo de teste gerado: {nome_arquivo}")
    else:
        print("⚠️ Não foi possível gerar o teste:")
        print(resposta_json.get("code", "Erro desconhecido."))


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2 and sys.argv[1] == "testar_conexao":
        testar_conexao_azure_openai()
        sys.exit(0)
    if len(sys.argv) != 3:
        print("Uso: python gerador_testes.py <arquivo_codigo.py> <arquivo_teste_saida.py>")
        print("Ou: python gerador_testes.py testar_conexao")
        print("Exemplo: python gerador_testes.py codigo.py testes_finais.py")
        sys.exit(1)
    caminho_codigo = sys.argv[1]
    caminho_teste = sys.argv[2]
    gerar_testes(caminho_codigo, caminho_teste)
