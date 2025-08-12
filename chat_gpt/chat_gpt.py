# coding: utf-8

from openai import OpenAI
from redis_adapter.redis_adapter import RedisAdapter
from time import sleep


class ChatGpt:
    """
    Classe para acessar a API ChatGPT
    """
    def __init__(self, config, logs):
        """
        Inicializa o objeto da ChatGPT
        :param config: Objeto de configuração
        :param logs: Objeto de log
        """
        self.config = config
        self.logs = logs

    def retorna_chave_chat_gpt_disponivel(self) -> str:
        """
        Retorna uma chave disponível para a utilização da API da ChatGPT (através da rotação das chaves)
        :return: Chave disponível para uso
        """
        try:
            redis = RedisAdapter(self.config.get('REDIS_DB_CONTROLES'))
            resultado = redis.retorna_chave_disponivel(self.config.get("REDIS_CHAT_GPT_KEYS_KEY"))
            redis.close()

            return resultado
        except Exception as ex:
            self.logs.error(f'Erro ao retornar a chave disponível - Error:{ex}')

    def envia_mensagem_chat(self, mensagem: str, json_format: bool = False, prefix: str = None, context: str = None, temperature: float = None) -> (str, int):
        """
        Envia uma mensagem para o chat do Chat GPT
        :param mensagem: Mensagem a ser enviada
        :param json_format: Formato da resposta
        :param prefix: Prefixo da mensagem
        :param context: Contexto da mensagem
        :param temperature: Temperatura da resposta
        :return: Resposta do chat e o total de tokens utilizados
        :rtype: (str, int)
        :raises Exception: Se ocorrer um erro ao enviar a mensagem ou se exceder o número de tentativas
        """
        retries = 0
        while retries < self.config.get('CHAT_GPT_RETRIES'):
            try:
                # Instanciando o objeto do mistral
                chave_chat_gpt = self.retorna_chave_chat_gpt_disponivel()
                client = OpenAI(api_key=chave_chat_gpt)

                # Criando o chat
                if prefix is not None:
                    if context is not None:
                        pergunta = [{"role": "system", "content": context}, {"role": "user", "content": mensagem}]
                    else:
                        pergunta = [{"role": "user", "content": mensagem}]
                else:
                    if context is not None:
                        pergunta = [{"role": "system", "content": context}, {"role": "user", "content": mensagem}]
                    else:
                        pergunta = [{"role": "user", "content": mensagem}]

                if json_format:
                    if temperature is not None:
                        chat_response = client.chat.completions.create(model=self.config.get("CHATGPT_AI_MODEL"), messages=pergunta, response_format={"type": "json_object"}, temperature=temperature)
                    else:
                        chat_response = client.chat.completions.create(model=self.config.get("CHATGPT_AI_MODEL"), messages=pergunta, response_format={"type": "json_object"})
                else:
                    if temperature is not None:
                        chat_response = client.chat.completions.create(model=self.config.get("CHATGPT_AI_MODEL"), messages=pergunta, response_format={"type": "text"}, temperature=temperature)
                    else:
                        chat_response = client.chat.completions.create(model=self.config.get("CHATGPT_AI_MODEL"), messages=pergunta, response_format={"type": "text"})

                # Processando a resposta
                retorno_chat_gpt = chat_response.choices[0].message.content
                retorno_chat_gpt = retorno_chat_gpt.strip()

                # Retornando o total de tokens
                total_tokens = chat_response.usage.total_tokens

                return retorno_chat_gpt, total_tokens
            except Exception as ex:
                # Em caso de erro faz o log e aguarda de maneira incremental com relação a tentativa
                self.logs.error(f'Erro ao enviar mensagem para o chat - Error:{ex}')
                retries += 1
                sleep(self.config.get('CHAT_GPT_TIMEOUT') * retries * self.config.get('CHAT_GPT_INCREASE_FACTORY'))

        # Caso estoure o limite de tentativas
        raise Exception('Erro ao enviar mensagem para o chat - Excedido o número de tentativas')
