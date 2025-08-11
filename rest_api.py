"""
Chatbot Banco de Preços - API RESTful
"""
# coding: utf-8

import json
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Request
from logger.logger import CustomLoggerMongoDB
from config import Config
from ai_middleware.ai_middleware import AIMiddleware
import uvicorn
import requests

logs = CustomLoggerMongoDB().get_logger()
config = Config().get_config()
app = FastAPI(title=config.get("TITULO"), description=config.get("DESCRICAO_API"), version=config.get("API_VERSION"), openapi_url="/openapi_espec_tec.json", debug=config.get("DEBUG"), logger=logs, servers=[],
              contact={"name": config.get("AUTOR"), "url": config.get("AUTOR_URL"), "email": config.get("AUTOR_EMAIL")}, terms_of_service="https://www.google.com.br",
              license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"})


class HealthCheck(BaseModel):
    """
    Classe de modelo para o health_check
    """
    status: str
    host: str
    port: int


class GenericHTTPError(BaseModel):
    """
    Classe de modelo genérico para erros HTTP
    """
    detail: str


class RetornoPadrao(BaseModel):
    """
    Classe de modelo padrão para retorno de sucesso
    """
    sumario: str
    texto: str


class PayloadPadrao(BaseModel):
    """
    Classe de modelo padrão para o payload entrada de dados
    """
    campo: str
    comando: str
    texto: str = ""


CUSTOM_RESPONSES = {400: {"content": {"application/json": {"example": {"detail": "string"}}}, "model": GenericHTTPError}, 401: {"content": {"application/json": {"example": {"detail": "string"}}}, "model": GenericHTTPError}}


def validar_token_api_auth(token: str) -> (bool, dict):
    """
    Função para validar o token de autenticação
    :param token: Token a ser validado
    :return: True se o token for válido, False se não for
    """
    try:
        # Validando se o token é uma string válida
        if token is None or token == "":
            return False, None

        # Uri da solicitação
        url = config.get("AUTH_TOKEN_URI")

        # Montando o payload
        payload = json.dumps({
            "token": token
        })

        # Montando o cabeçalho
        headers = {
            'Content-Type': 'application/json'
        }

        # Chamando a API de autenticação
        response = requests.request("POST", url, headers=headers, data=payload)

        # Verificando o status da resposta
        if response.status_code == 200:
            response = json.loads(response.content)
            if response.get("valid"):
                return True, response.get("payload")

        # Se o status não for 200 e/ou for inválido, retornar False e None
        return False, None
    except Exception as ex:
        error = f"Erro ao validar o token de autenticação: {ex}"
        logs.error(error)
        return False, None


@app.get("/health_check", tags=[config.get("TITULO")])
async def health_check() -> HealthCheck:
    """
    Endpoint de health check da API
    """
    return HealthCheck(status="OK", host=config.get("HOST"), port=config.get("PORT"))


@app.post("/chatbot", tags=[config.get("TITULO")], responses=CUSTOM_RESPONSES)
async def chatbot(body: PayloadPadrao, request: Request) -> RetornoPadrao:
    """
    Recebe um comando do usuário, um texto se disponível do campo e o nome do campo para o qual se deseja fazer a inferência da resposta do chatbot
    """
    try:
        # Lendo o cabeçalho e validando o token
        token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
        valido, payload = validar_token_api_auth(token=token)
        if not valido:
            raise HTTPException(status_code=401, detail="Token inválido ou expirado.")

        body_dict = body.model_dump()

        ai_middleware = AIMiddleware(config=config, logs=logs)

        sumario, texto, tokens = ai_middleware.inferir_chatbot_from_context(body_dict)

        # Logando consumo de tokens
        logs.success({"requisitor": payload, "tokens": tokens})

        return RetornoPadrao(sumario=sumario, texto=texto)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        mensagem = f"Erro ao processar a chamada: {body.model_dump()}. Error: {ex}"
        logs.error(mensagem)
        raise HTTPException(status_code=500, detail=mensagem)


if __name__ == "__main__":
    """
    Inicia a API RESTful com Uvicorn
    """
    try:
        logs.debug(f"Iniciando API - Especificação Técnica :: {config.get('TITULO')} - {config.get('DESCRICAO_API')} - {config.get('API_VERSION')}")
        uvicorn.run("rest_api:app", host=config.get("HOST"), port=config.get("PORT"), workers=config.get("WORKERS"), log_level=config.get("UVICORN_RUN_LOG_LEVEL"), use_colors=True)
    except Exception as ex:
        logs.error(f"Erro ao iniciar a API: {ex}")
        exit(1)
