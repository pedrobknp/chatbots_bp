"""
MongoDB Class para as operações de banco de dados MongoDB
"""
# coding: utf-8

from config import Config
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

config = Config().get_config()


class MongoDB:
    """
    Classe para manipulação de banco de dados MongoDB
    """

    def __init__(self, collection=None):
        """
        Inicializa conexão com o MongoDB
        """
        self.host = config.get('MONGODB_HOST')
        self.port = int(config.get('MONGODB_PORT'))
        self.user = config.get('MONGODB_USER')
        self.password = config.get('MONGODB_PASSWD')
        self.db_name = config.get('MONGODB_DB')
        self.collection_name = collection if collection is not None else config.get('MONGODB_COLLECTION')
        self.conn = MongoClient(host=self.host, port=self.port, username=self.user, password=self.password, authSource=self.db_name)
        self.db = self.conn[self.db_name]
        self.collection = self.db[self.collection_name]

    def get_conn(self):
        """
        Retorna conexão com o MongoDB
        :return: MongoDB connection object
        """
        try:
            return self.conn
        except ConnectionFailure as err:
            raise err

    def get_collection(self):
        """
        Retorna collection do MongoDB
        :return: MongoDB connection object
        """
        try:
            return self.collection
        except Exception as err:
            raise err

    def close(self):
        """
        Fecha conexão com o MongoDB
        :return: None
        """
        self.conn.close()

    def delete_collection(self):
        """
        Deleta a collection do MongoDB
        :return: None
        """
        self.collection.drop()

    def delete_db(self):
        """
        Deleta o banco de dados do MongoDB
        :return: Bool (True or False)
        """
        try:
            self.conn.drop_database(self.db_name)
            return True
        except Exception as err:
            raise err

    def insert_into_collection(self, data):
        """
        Insere dados na collection do MongoDB
        :param data: Dados a serem inseridos
        :return: Retorna ID dinâmico do MongoDB do log inserido
        """
        try:
            result = self.collection.insert_one(data)
            return result.inserted_id
        except Exception as err:
            raise err

    def find_one(self, query):
        """
        Busca um documento na collection do MongoDB
        :param query: Query a ser usada na busca
        :return: Documento encontrado
        """
        try:
            result = self.collection.find_one(query)
            return result
        except Exception as err:
            raise err

    def insert_many_into_collection(self, data):
        """
        Insere vários dados na collection do MongoDB
        :param data: Dados a serem inseridos
        :return: Retorna ID dinâmico do MongoDB do log inserido
        """
        try:
            result = self.collection.insert_many(data)
            return result.inserted_ids
        except Exception as err:
            raise err

    def find(self, query):
        """
        Busca documentos na collection do MongoDB
        :param query: Query a ser usada na busca
        :return: Documentos encontrados
        """
        try:
            result = self.collection.find(query)
            return result
        except Exception as err:
            raise err

    def find_all(self):
        """
        Busca todos os documentos na collection do MongoDB
        :return: Documentos encontrados
        """
        try:
            result = self.collection.find()
            return result
        except Exception as err:
            raise err

    def delete_one(self, query) -> int:
        """
        Deleta um documento na collection do MongoDB
        :param query: Query a ser usada na busca
        :return: int quantidade de documentos deletados
        """
        try:
            result = self.collection.delete_one(query)
            return result.deleted_count
        except Exception as err:
            raise err

    def delete_many(self, query):
        """
        Deleta vários documentos na collection do MongoDB
        :param query: Query a ser usada na busca
        :return: None
        """
        try:
            self.collection.delete_many(query)
        except Exception as err:
            raise err

    def update_one(self, query, new_values):
        """
        Atualiza um documento na collection do MongoDB
        :param query: Query a ser usada na busca
        :param new_values: Novos valores a serem inseridos (deve incluir operadores como $set)
        :return: Número de documentos modificados
        """
        try:
            result = self.collection.update_one(query, new_values, upsert=True)
            return result.modified_count
        except Exception as err:
            raise err

    def update_many(self, query, new_values):
        """
        Atualiza vários documentos na collection do MongoDB
        :param query: Query a ser usada na busca
        :param new_values: Novos valores a serem inseridos
        :return: None
        """
        try:
            self.collection.update_many(query, new_values)
        except Exception as err:
            raise err

    def count_documents(self, query):
        """
        Conta documentos na collection do MongoDB
        :param query: Query a ser usada na busca
        :return: Quantidade de documentos encontrados
        """
        try:
            result = self.collection.count_documents(query)
            return result
        except Exception as err:
            raise err

    def aggregate(self, pipeline):
        """
        Agrega documentos na collection do MongoDB
        :param pipeline: Pipeline a ser usada na busca
        :return: Documentos encontrados
        """
        try:
            result = self.collection.aggregate(pipeline)
            return result
        except Exception as err:
            raise err

    def create_index(self, index):
        """
        Cria index na collection do MongoDB
        :param index: Index a ser criado
        :return: None
        """
        try:
            self.collection.create_index(index)
        except Exception as err:
            raise err

    def create_indexes(self, indexes):
        """
        Cria indexes na collection do MongoDB
        :param indexes: Indexes a serem criados
        :return: None
        """
        try:
            self.collection.create_indexes(indexes)
        except Exception as err:
            raise err

    def drop_index(self, index):
        """
        Deleta index na collection do MongoDB
        :param index: Index a ser deletado
        :return: None
        """
        try:
            self.collection.drop_index(index)
        except Exception as err:
            raise err

    def drop_indexes(self):
        """
        Deleta todos os indexes na collection do MongoDB
        :return: None
        """
        try:
            self.collection.drop_indexes()
        except Exception as err:
            raise err

    def list_indexes(self):
        """
        Lista todos os indexes na collection do MongoDB
        :return: Indexes encontrados
        """
        try:
            result = self.collection.list_indexes()
            return result
        except Exception as err:
            raise err

    def reindex(self):
        """
        Reindexa a collection do MongoDB
        :return: None
        """
        try:
            self.collection.reindex()
        except Exception as err:
            raise err

    def index_information(self):
        """
        Informações do index na collection do MongoDB
        :return: Informações do index
        """
        try:
            result = self.collection.index_information()
            return result
        except Exception as err:
            raise err

    def create_collection(self, collection):
        """
        Cria collection no MongoDB
        :param collection: Collection a ser criada
        :return: None
        """
        try:
            self.db.create_collection(collection)
        except Exception as err:
            raise err

    def list_collections(self):
        """
        Lista collections no MongoDB
        :return: Collections encontradas
        """
        try:
            result = self.db.list_collection_names()
            return result
        except Exception as err:
            raise err

    def check_collection(self, collection):
        """
        Verifica se a collection existe no MongoDB
        :param collection: Collection a ser verificada
        :return: Bool (True or False)
        """
        try:
            result = collection in self.db.list_collection_names()
            return result
        except Exception as err:
            raise err

    def check_db(self):
        """
        Verifica se o banco de dados existe no MongoDB
        :return: Bool (True or False)
        """
        try:
            result = self.db_name in self.conn.list_database_names()
            return result
        except Exception as err:
            raise err

    def check_index(self, index):
        """
        Verifica se o index existe na collection do MongoDB
        :param index: Index a ser verificado
        :return: Bool (True or False)
        """
        try:
            result = index in self.collection.index_information()
            return result
        except Exception as err:
            raise err

    def set_collection(self, collection):
        """
        Seta a collection do MongoDB
        :param collection: Collection a ser setada
        :return: None
        """
        try:
            self.collection_name = collection
            self.collection = self.db[self.collection_name]
        except Exception as err:
            raise err

    def flush_db(self):
        """
        Limpa o banco de dados do MongoDB
        :return: None
        """
        try:
            self.db.drop()
        except Exception as err:
            raise err

    def flush_collection(self):
        """
        Limpa a collection do MongoDB
        :return: None
        """
        try:
            self.collection.drop()
        except Exception as err:
            raise err

    def sync_db(self):
        """
        Sincroniza o banco de dados do MongoDB
        :return: None
        """
        try:
            self.conn.admin.command('resync')
        except Exception as err:
            raise err

    def sync_collection(self):
        """
        Sincroniza a collection do MongoDB
        :return: None
        """
        try:
            self.collection.sync()
        except Exception as err:
            raise err
