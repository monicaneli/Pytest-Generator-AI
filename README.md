# Pytest-Generator-AI

> Geração automática de testes unitários com IA para código Python usando LangChain e Azure OpenAI.

## Descrição

O **Pytest-Generator-AI** é um agente de IA que, a partir de um arquivo Python de código-fonte (`codigo.py`), gera automaticamente um arquivo de testes unitários (`test_codigo.py`) no padrão pytest. Utiliza LangChain e Azure OpenAI para criar funções de teste que cobrem cenários de sucesso e falha, promovendo qualidade e automação no desenvolvimento.

## Funcionalidades
- Geração automática de testes pytest para qualquer código Python.
- Cobertura de casos de sucesso e falha.
- Integração com Azure OpenAI (GPT-4).
- Interface de linha de comando simples.

## Dependências
- Python 3.8+
- [langchain-openai](https://pypi.org/project/langchain-openai/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [pytest](https://pypi.org/project/pytest/)

Instale todas as dependências com:

```bash
pip install -r requirements.txt
```

## Configuração

1. **Crie o arquivo `.env` na raiz do projeto:**

```
AZURE_OPENAI_API_KEY=chave_da_api
AZURE_OPENAI_ENDPOINT=https://<seu-endpoint>.openai.azure.com/
AZURE_OPENAI_API_VERSION=2023-12-01-preview
AZURE_OPENAI_DEPLOYMENT_NAME=<nome_da_deployment>
```

2. **Como obter as credenciais Azure:**
   1. Acesse o [Portal Azure](https://portal.azure.com/).
   2. Crie ou acesse um recurso "Azure OpenAI".
   3. Implemente um modelo GPT-4 com suporte a imagens.
   4. No "Playground de chat", clique em "Exibir código" para copiar as credenciais.

## Como usar

1. **Gere um arquivo de código Python de exemplo:**

O arquivo com o código, contendo as funções, para as quais serão gerados os testes unitários. 

2. **Execute o gerador de testes:**

```bash
python gerador_testes.py Exemplos/codigo.py Exemplos/testes_finais.py
```

O arquivo de teste será salvo no caminho informado, mesmo que a pasta não exista.

3. **Testar a conexão com Azure OpenAI:**

```bash
python gerador_testes.py testar_conexao
```

## Como rodar os testes gerados

Após gerar o arquivo de testes, execute:

```bash
pytest Exemplos/testes_finais.py
```

## Estrutura do Projeto

```
Pytest-Generator-AI/
├── Exemplos/
│   ├── codigo.py
│   └── testes_finais.py
├── gerador_testes.py
├── requirements.txt
├── .env
└── README.md
```

## Licença

MIT