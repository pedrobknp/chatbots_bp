"""
Classe para manipular os dados de contexto dos campos para o chatbot genérico BP
"""
# coding: utf-8

from mongo.mongo import MongoDB
from config import Config

config = Config().get_config()


class ContextModel:
    """
    Classe responsável por gerenciar o contexto dos campos no MongoDB
    Esta classe utiliza a classe MongoDB para inserir e recuperar contextos dos campos no banco de dados.
    """
    def __init__(self, logs):
        self.mongo = MongoDB(collection=config.get("MONGODB_COLLECTION_CONTEXT"))
        self.logs = logs
        self.campos_validar = ["field", "context", "limit"]

    def insert_context(self, context):
        """
        Insere o contexto dos campos no MongoDB
        :param context: Contexto a ser inserido
        :return: Retorna ID dinâmico do MongoDB do contexto inserido
        :rtype: ID do contexto inserido
        :raises Exception: Se ocorrer um erro ao inserir o contexto no MongoDB
        """
        try:
            if not isinstance(context, dict):
                raise Exception(f'Contexto inválido para inserir: {context}')

            if not all(key in context for key in self.campos_validar):
                raise Exception(f'Campos inválidos para inserir contexto: {context}')

            # Verifica se o campo já existe
            if self.mongo.find_one({"field": context.get("field")}):
                raise Exception(f'Campo já existe: {context.get("field")}')

            result = self.mongo.insert_into_collection(context)
            return result
        except Exception as e:
            self.logs.error(f'Erro ao inserir contexto no mongodb - Error:{e}')

    def get_context(self, field: str):
        """
        Recupera o contexto dos campos do MongoDB
        :param field: Campo para o qual se deseja recuperar o contexto
        :return: Retorna o contexto do campo
        :rtype: Dicionário com o contexto do campo
        :raises Exception: Se ocorrer um erro ao recuperar o contexto do MongoDB ou se o contexto não for encontrado
        """
        try:
            result = self.mongo.find_one({"field": field})

            if not result:
                raise Exception(f'Contexto não encontrado para o campo: {field}')

            return result
        except Exception as e:
            self.logs.error(f'Erro ao recuperar contexto do mongodb - Error:{e}')

    def close_connection(self):
        """
        Fecha a conexão com o MongoDB
        """
        self.mongo.close()
