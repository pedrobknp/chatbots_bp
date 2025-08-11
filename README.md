# Introdução 
PROJETO DA API PARA CHATBOT BANCO DE PREÇOS

# Tecnologias
- Python 3.12
- FastAPI
- Pydantic
- Uvicorn
- Redis
- MongoDB
- OpenAI (API Library)
- Docker (Opcional)

# Instalação

Instalar o enviroment para a Aplicação. Instalar as dependências diretamente com o arquivo requirements.txt:

```conda create -n "[nome_do_env]" python=3.12```

```conda activate "[nome_do_env]"```

```python -m pip install --upgrade pip```

```pip install -r requirements.txt```

# Configuração

Ajustar as configurações no arquivo .env
Validando os endereços, portas e credênciais para os serviços do Redis e MongoDB. 
As chaves de acesso para as APIs do OpenAI.

# Execução

Executar o comando para iniciar a api:

```python rest_api.py```

# Publicação

Para publicar a API, basta fazer uma PR no branch main do repositório. Que a trigger de deploy será executada automaticamente.
