"""
Custom Logger Module
"""
# coding: utf-8

from loguru import logger
from datetime import datetime
from models.logs_model import LogsModel
import warnings
import sys


warnings.filterwarnings('ignore')


class CustomLogger:
    """
    Classe CustomLogger para criar um logger customizado com Loguru.
    """
    def __init__(self, identificador: str = None):
        """
        Inicializa o logger
        :param identificador: Identificador do logger para diferenciar arquivos de serviços diferentes
        """
        self.logger = logger
        self.logger.remove()
        self.logger.add(sys.stdout, level="DEBUG")
        self.logger.add(f"./logs/app_{datetime.now().strftime('%d_%m_%y_%HH_%MM_%SS')}.log" if identificador is None else f"./logs/app_{identificador}_{datetime.now().strftime('%d_%m_%y_%HH_%MM_%SS')}.log", level="DEBUG")

    def get_logger(self):
        """
        Retorna o logger
        :return: Logger object
        """
        return self.logger


class CustomLoggerMongoDB:
    """
    Classe CustomLoggerMongoDB para criar um logger customizado com Loguru que envia logs para o MongoDB.
    """
    def __init__(self):
        """
        Inicializa um Custom Logger para o processamento de logs no MongoDB
        """
        self.logger = logger
        self.logger.remove()
        self.logger.add(sys.stdout, level="DEBUG")
        self.logs = LogsModel()
        self.logger.add(self.mongo_handler(), level="DEBUG", format="{message}")

    def mongo_handler(self):
        """
        Retorna um handler para o MongoDB
        :return: Uma função de handler que formata a mensagem de log e manda para o MongoDB
        """
        def handler(message):
            """
            Função de handler que formata a mensagem de log e manda para o MongoDB
            :param message:
            """
            record = message.record
            log = {
                "time": record["time"].replace(tzinfo=None),
                "level": record["level"].name,
                "message": record["message"],
                "file": record["file"].name,
                "line": record["line"],
                "module": record["function"],
                "function": record["name"]
            }
            self.logs.insert_log_mongodb(log)
        return handler

    def get_logger(self):
        """
        Retorna o logger
        :return: Logger object
        """
        return self.logger

    def logger_close_mongo(self):
        """
        Fecha o logger
        """
        self.logger.remove()
        self.logs.close_connection()
