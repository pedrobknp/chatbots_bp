"""
Adaptador para o Redis
"""
# coding: utf-8

from redis import Redis
from config import Config
import hashlib

config = Config().get_config()


class RedisAdapter:
    """
    Classe adaptadora para o Redis, facilitando a interação com o banco de dados
    """

    def __init__(self, db: int = 0):
        """
        Inicializa a conexão com o Redis
        :param db: Número do banco de dados a ser utilizado
        """
        self.host = config.get('REDIS_HOST')
        self.port = config.get('REDIS_PORT')
        self.pwd = config.get('REDIS_PWD')
        self.db = db
        if self.pwd is None or self.pwd == '':
            self.conn = Redis(host=self.host, port=self.port, db=self.db, protocol=3)
        else:
            self.conn = Redis(host=self.host, port=self.port, db=self.db, password=self.pwd, protocol=3)
        self.pipeline = None

    def get_conn(self):
        """
        Retorna a conexão com o Redis
        :return: Redis connection object
        """
        try:
            return self.conn
        except Exception as e:
            raise e

    def get(self, key):
        """
        Retorna o valor de uma chave (dict) no Redis
        :param key: Chave a ser consultada
        :return: Valor da chave
        """
        try:
            return self.conn.get(name=key)
        except Exception as e:
            raise e

    def set_value(self, value):
        """
        Seta um valor para uma chave no Redis
        :param value: Valor a ser setado
        :return: Identificador do set
        """
        try:
            # Forçando valores no redis a serem sempre minusculos e sem espaços
            chave = value.lower().strip()

            return self.conn.set(name=chave, value=value, nx=True)
        except Exception as e:
            raise e

    def set_pipeline(self):
        """
        Inicia a pipeline para execução de operações em lote
        """
        try:
            self.pipeline = self.conn.pipeline()
        except Exception as e:
            raise e

    def set_value_pipeline(self, value):
        """
        Seta um valor para uma chave no Redis utilizando um pipeline
        :param value: Valor a ser setado
        """
        try:
            # Forçando valores no redis a serem sempre minusculos e sem espaços
            value = value.lower().strip()

            # Gerar md5 para validar a existencia da sentença e usar como chave
            chave = hashlib.md5(value.encode()).hexdigest()

            self.pipeline.set(name=chave, value=value, nx=True)
        except Exception as e:
            raise e

    def execute_pipeline(self):
        """
        Executa as operações em lote do pipeline
        """
        try:
            self.pipeline.execute()
        except Exception as e:
            raise e

    def delete(self, keys):
        """
        Deleta uma chave no Redis
        :param keys: Chaves a serem deletadas
        :return: Status da operação
        """
        try:
            return self.conn.delete(keys)
        except Exception as e:
            raise e

    def exists(self, key):
        """
        Verifica se uma chave existe no Redis
        :param key: Chaves a serem verificadas
        :return: Status da operação
        """
        try:
            # Forçando valores no redis a serem sempre minusculos e sem espaços
            chave = key.lower().strip()

            return bool(self.conn.exists(chave))
        except Exception as e:
            raise e

    def get_all_keys(self):
        """
        Retorna todas as chaves do Redis
        :return: Lista de chaves
        """
        try:
            return self.conn.keys()
        except Exception as e:
            raise e

    def get_keys_paginated(self, cursor=0, count=1000):
        """
        Retorna as chaves do Redis de forma paginada
        :param cursor: Cursor de início
        :param count: Quantidade de chaves a serem retornadas
        :return: Lista de chaves
        """
        try:
            return self.conn.scan(cursor=cursor, count=count)
        except Exception as e:
            raise e

    def atualiza_consumo_tokens_mistral(self, tokens: int):
        """
        Atualiza o consumo de tokens da Mistral
        :param tokens: Quantidade de tokens consumidos
        """
        try:
            if tokens is None or tokens == 0:
                raise Exception('Quantidade de tokens inválida')

            self.conn.incrby(name=config.get("REDIS_MISTRAL_TOKENS_KEY"), amount=tokens)
        except Exception as ex:
            raise ex

    def retorna_chave_mistral_disponivel(self):
        """
        Retorna uma chave disponível para a utilização da API da Mistral (através da rotação das chaves)
        :return: Chave disponível para uso
        """
        try:
            if config.get("MISTRAL_AI_KEYS") is None or config.get("MISTRAL_AI_KEYS") == '':
                raise Exception('Chaves da Mistral não configuradas')

            # Verificando se as chaves estão no Redis
            if not self.conn.exists(config.get("REDIS_MISTRAL_KEYS_KEY")):
                for chave in config.get("MISTRAL_AI_KEYS").strip().split(','):
                    self.conn.sadd(config.get("REDIS_MISTRAL_KEYS_KEY"), chave)

            # Retornando a chave disponível
            chave = self.conn.srandmember(config.get("REDIS_MISTRAL_KEYS_KEY"))

            return chave
        except Exception as ex:
            raise ex

    def retorna_chave_disponivel(self, keys_key: str):
        """
        Retorna uma chave disponível para a utilização das APIS de IA (através da rotação das chaves)
        :param keys_key: Chave no Redis onde as chaves estão armazenadas
        :return: Chave disponível para uso
        """
        try:
            # Verificando se as chaves estão no Redis
            if not self.conn.exists(keys_key):
                raise Exception(f'Chaves não encontradas no Redis para a key: {keys_key}')

            # Retornando a chave disponível
            chave = self.conn.srandmember(keys_key)

            return chave.decode('utf-8')
        except Exception as ex:
            raise ex

    def close(self):
        """
        Fecha a conexão com o Redis
        """
        try:
            self.conn.close()
        except Exception as e:
            raise e

    def flush_db(self):
        """
        Limpa o banco de dados do Redis
        """
        try:
            self.conn.flushdb()
        except Exception as e:
            raise e
