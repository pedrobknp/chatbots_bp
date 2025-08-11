"""
LogsModel
"""
# coding: utf-8

from mongo.mongo import MongoDB
from config import Config

config = Config().get_config()


class LogsModel:
    """
    Classe responsável por gerenciar os logs no MongoDB
    Esta classe utiliza a classe MongoDB para inserir logs no banco de dados.
    Ela é inicializada com a coleção de logs definida na configuração.
    A classe oferece métodos para inserir logs e fechar a conexão com o MongoDB.
    A inserção de logs é feita através do método `insert_log_mongodb`, que recebe
    um log como parâmetro e retorna o ID do documento inserido no MongoDB.
    """
    def __init__(self):
        self.mongo = MongoDB(collection=config.get("MONGODB_COLLECTION_LOGS"))

    def insert_log_mongodb(self, log):
        """
        Insere logs gerados pelo Loguru para o MongoDB
        :param log: Log a ser usado na inserção
        :return: Retorna ID dinâmico do MongoDB do log inserido
        """
        try:
            result = self.mongo.insert_into_collection(log)

            return result
        except Exception as e:
            print(f'Erro ao inserir log no mongodb - Error:{e}')

    def close_connection(self):
        """
        Fecha a conexão com o MongoDB
        """
        self.mongo.close()
