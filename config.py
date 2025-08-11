"""
Configuração do ambiente para a aplicação
"""
# coding: utf-8

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Classe de configuração que carrega as variáveis de ambiente
    """
    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT")
    WORKERS = os.getenv("WORKERS")
    DEBUG = os.getenv("DEBUG")
    SECRET_KEY = os.getenv("SECRET_KEY")
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")
    REDIS_DB_CONTROLES = os.getenv("REDIS_DB_CONTROLES")
    REDIS_ENCODING = os.getenv("REDIS_ENCODING")
    REDIS_PWD = os.getenv("REDIS_PWD")
    MONGODB_HOST = os.getenv("MONGODB_HOST")
    MONGODB_PORT = os.getenv("MONGODB_PORT")
    MONGODB_USER = os.getenv("MONGODB_USER")
    MONGODB_PASSWD = os.getenv("MONGODB_PASSWD")
    MONGODB_DB = os.getenv("MONGODB_DB")
    MONGODB_COLLECTION_CONTEXT = os.getenv("MONGODB_COLLECTION_CONTEXT")
    MONGODB_COLLECTION_LOGS = os.getenv("MONGODB_COLLECTION_LOGS")
    CHATGPT_AI_MODEL = os.getenv("CHATGPT_AI_MODEL")
    CHAT_GPT_API_KEYS = os.getenv("CHAT_GPT_API_KEYS")
    CHAT_GPT_RETRIES = os.getenv("CHAT_GPT_RETRIES")
    CHAT_GPT_TIMEOUT = os.getenv("CHAT_GPT_TIMEOUT")
    CHAT_GPT_INCREASE_FACTORY = os.getenv("CHAT_GPT_INCREASE_FACTORY")
    CHAT_GPT_MAX_TOKENS = os.getenv("CHAT_GPT_MAX_TOKENS")
    REDIS_CHAT_GPT_KEYS_KEY = os.getenv("REDIS_CHAT_GPT_KEYS_KEY")
    REDIS_CHAT_GPT_TOKENS_KEY = os.getenv("REDIS_CHAT_GPT_TOKENS_KEY")
    TITULO = os.getenv("TITULO")
    DESCRICAO_API = os.getenv("DESCRICAO_API")
    API_VERSION = os.getenv("API_VERSION")
    AUTOR = os.getenv("AUTOR")
    AUTOR_EMAIL = os.getenv("AUTOR_EMAIL")
    AUTOR_URL = os.getenv("AUTOR_URL")
    AUTH_TOKEN_URI = os.getenv("AUTH_TOKEN_URI")
    UVICORN_RUN_LOG_LEVEL = os.getenv("UVICORN_RUN_LOG_LEVEL")
    TEMPERATURE_CHATBOT = os.getenv("TEMPERATURE_CHATBOT")

    def get_config(self):
        """
        Retorna as configurações do env
        :return: Dicionário com as configurações
        """

        return {
            "HOST": self.HOST,
            "PORT": int(self.PORT),
            "WORKERS": int(self.WORKERS),
            "DEBUG": bool(self.DEBUG),
            "SECRET_KEY": self.SECRET_KEY,
            "REDIS_HOST": self.REDIS_HOST,
            "REDIS_PORT": int(self.REDIS_PORT),
            "REDIS_DB_CONTROLES": int(self.REDIS_DB_CONTROLES),
            "REDIS_ENCODING": self.REDIS_ENCODING,
            "REDIS_PWD": self.REDIS_PWD,
            "MONGODB_HOST": self.MONGODB_HOST,
            "MONGODB_PORT": int(self.MONGODB_PORT),
            "MONGODB_USER": self.MONGODB_USER,
            "MONGODB_PASSWD": self.MONGODB_PASSWD,
            "MONGODB_DB": self.MONGODB_DB,
            "MONGODB_COLLECTION_CONTEXT": self.MONGODB_COLLECTION_CONTEXT,
            "MONGODB_COLLECTION_LOGS": self.MONGODB_COLLECTION_LOGS,
            "CHATGPT_AI_MODEL": self.CHATGPT_AI_MODEL,
            "CHAT_GPT_API_KEYS": self.CHAT_GPT_API_KEYS,
            "CHAT_GPT_RETRIES": int(self.CHAT_GPT_RETRIES),
            "CHAT_GPT_TIMEOUT": int(self.CHAT_GPT_TIMEOUT),
            "CHAT_GPT_INCREASE_FACTORY": float(self.CHAT_GPT_INCREASE_FACTORY),
            "CHAT_GPT_MAX_TOKENS": int(self.CHAT_GPT_MAX_TOKENS),
            "REDIS_CHAT_GPT_KEYS_KEY": self.REDIS_CHAT_GPT_KEYS_KEY,
            "REDIS_CHAT_GPT_TOKENS_KEY": self.REDIS_CHAT_GPT_TOKENS_KEY,
            "TITULO": self.TITULO,
            "DESCRICAO_API": self.DESCRICAO_API,
            "API_VERSION": self.API_VERSION,
            "AUTOR": self.AUTOR,
            "AUTOR_EMAIL": self.AUTOR_EMAIL,
            "AUTOR_URL": self.AUTOR_URL,
            "AUTH_TOKEN_URI": self.AUTH_TOKEN_URI,
            "UVICORN_RUN_LOG_LEVEL": self.UVICORN_RUN_LOG_LEVEL,
            "TEMPERATURE_CHATBOT": float(self.TEMPERATURE_CHATBOT)
        }
