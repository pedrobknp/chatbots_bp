"""
Classe com o middleware para a IA - Isolando a lógica de inferência da IA das API's utilizadas
"""
# coding: utf-8

from chat_gpt.chat_gpt import ChatGpt
from models.context_model import ContextModel
import json


class AIMiddleware:
    """
    Classe responsável por isolar a lógica de inferência da IA das API's utilizadas
    """
    def __init__(self, config, logs):
        self.config = config
        self.logs = logs
        self.chat_gpt = ChatGpt(config, logs)

    def inferir_chat_gpt(self, mensagem: str, json_format: bool = False, prefix: str = None, context: str = None, temperature: float = None) -> (str, int):
        """
        Envia uma mensagem para o chat da GPT
        :param mensagem: Mensagem a ser enviada
        :param json_format: Formato da resposta
        :param prefix: Prefixo da mensagem
        :param context: Contexto da mensagem
        :param temperature: Temperatura da resposta
        :return: Resposta do chat
        """
        return self.chat_gpt.envia_mensagem_chat(mensagem, json_format, prefix, context, temperature)

    def inferir(self, mensagem: str, json_format: bool = False, prefix: str = None, context: str = None, temperature: float = None) -> (str, int):
        """
        Envia uma mensagem para o chat da Mistral ou GPT
        :param mensagem: Mensagem a ser enviada
        :param json_format: Formato da resposta
        :param prefix: Prefixo da mensagem
        :param context: Contexto da mensagem
        :param temperature: Temperatura da resposta
        :return: Resposta do chat
        """
        total_tokens = 0
        resultado = None
        try:
            resultado, total_tokens = self.inferir_chat_gpt(mensagem, json_format, prefix, context, temperature)

            if resultado is not None and resultado != "":
                resultado = resultado.strip()
        except Exception as ex:
            self.logs.error(f'Erro ao inferir: {ex}')
        finally:
            return resultado, total_tokens

    def inferir_chatbot(self, mensagem_chatbot: str, prompt_assistente: str) -> (str, str, int):
        """
        Envia o comando do usuário, mas o contexto do agente para fazer a inferência da resposta do chatbot
        :param mensagem_chatbot: Mensagem completa para o chatbot com todos os dados do campo conhecidos e fornecidos pelo usuário.
        :param prompt_assistente: Prompt do assistente (Prompt para tornar o assistente em um chatbot especializado para cada item).
        :return: Resposta do chat contendo o sumário da alteração executada na resposta e a resposta com o texto do campo ajustado.
        Retorna também o total de tokens utilizados na inferência.
        """
        try:
            resposta, total_tokens = self.inferir(mensagem=mensagem_chatbot, json_format=True, context=prompt_assistente, temperature=self.config.get("TEMPERATURE_CHATBOT"))

            # Tratando o retorno
            try:
                resposta = json.loads(resposta.strip())
            except Exception as ex:
                error = f'Erro ao converter a resposta para o formato correto: {ex}'
                raise Exception(error)

            # Retornando o resultado final
            if isinstance(resposta, dict):
                return resposta.get("sumario", None), resposta.get("texto", None), total_tokens
            else:
                return resposta, None, total_tokens
        except Exception as ex:
            self.logs.error(f"Erro chatbot: {ex}")
            raise ex

    def inferir_chatbot_from_context(self, chatbot: dict) -> (str, str, int):
        """
        Inferência a partir do contexto do campo informado e das informações enviadas pelo usuário.
        :param chatbot: Dados do chatbot quando for necessário utilizar o chatbot para inferir a descrição
        :return: Sumário da alteração, valor do campo ajustado e total de tokens utilizados na inferência.
        """
        try:
            # buscando o contexto do chatbot
            nome_campo = chatbot.get("campo")
            context_model = ContextModel(logs=self.logs)
            context = context_model.get_context(field=nome_campo)
            context_model.close_connection()

            if not context:
                raise Exception(f'Contexto não encontrado para o campo: {nome_campo}')

            # Separando os valores para o chatbot
            contexto = context.get("context")
            limite = context.get("limit")

            # Preparando o chatbot
            prompt_chatbot = f"""Tendo como nome do campo: '{nome_campo.strip()}'\n 
            Tendo como contexto do campo: '{contexto.strip()}'\n
            Tendo como limite de caracteres do campo: {int(limite)}\n
            Tendo como valor atual do campo: '{chatbot.get("texto", "").strip()}'\n
            Tendo como comando do usuário: '{chatbot.get("comando").strip()}'\n
            Seguindo a sua orientação como chatbot do sistema Banco de Preços. Especializado em automatizar o preenchimento de alguns campos em diversos formulários da plataforma.
            Retorne o sumário da alteração e o texto criado/ajustado para os dados do campo e comando informados.
            Observações: 
            - Se o limite for igual a zero (0). Significa que o campo não possui limite de caracteres, ou seja, pode ser preenchido com qualquer quantidade de caracteres.
            - Se o texto for vazio, significa que o campo não possui valor atual preenchido, ou seja, está em branco. Você deve preencher o campo seguindo o comando do usuário, e as informações recebidas sobre o campo, caso seja possível criar o texto a partir dessas informações.
            """

            prompt_assistente = """Você é um chatbot do sistema Banco de Preços. Especializado em automatizar o preenchimento de alguns campos em diversos formulários da plataforma.
            Você vai receber como entrada o nome do campo no formulário (o valor da tag name do form html), o contexto do campo (uma descrição do que é o campo, sua importância e significado e/ou como ele deve ser preenchido), o limite de caracteres do campo (quantidade máxima de caracteres que o campo aceita), e se houver, o valor atual do campo (o valor que está atualmente preenchido no campo) que deverá ser ajustado a partir do comando do usuário.
            Além dessas entradas referentes ao campo, você também vai receber o comando do usuário (uma instrução de como o usuário deseja que o campo seja preenchido ou ajustado).
            Com base nessas entradas você vai ajustar o valor do campo seguindo o comando do usuário.
            Os ajustes serão feitos seguindo o comando enviado pelo usuário e as informações do campo, principalmente o contexto, que vai definir de que se trata e como deve ser preenchido o campo.
            Se o comando do usuário não tiver relação com o texto e/ou o contexto do campo, ou não for claro você deve retornar uma mensagem informando que não foi possível entender o comando, no sumário e retornar o texto em branco.
            Você sempre irá responder com um Json contendo o sumário da alteração executada e o texto criado/ajustado.
            O sumário da alteração será uma descrição curta e objetiva do que foi executado.
            O texto criado/ajustado será o valor do campo ajustado, seguindo o comando do usuário e as informações do campo.
            No Json de retorno o sumário da alteração estará na chave ("sumario") e o texto criado/ajustado estará na chave ("texto")."""

            # Chamando o chatbot com todos os parâmetros
            sumario, resposta, total_tokens = self.inferir_chatbot(mensagem_chatbot=prompt_chatbot.strip(), prompt_assistente=prompt_assistente.strip())

            if sumario is None or sumario == "":
                raise Exception(f'Não foi possível inferir a solicitação do chat: {chatbot.get("message", None)}')

            return sumario, resposta, total_tokens
        except Exception as ex:
            self.logs.error(f'Erro ao inferir a descrição da necessidade: {ex}')
            raise ex


    def inferir_reescrita_completa(self, texto: str) -> str:
        """
        Infere a reescrita de um texto
        :param texto: Texto a ser reescrito
        :return: Texto reescrito
        """
        try:
            # Selecionando os prompts para: rewrite / reescrita
            prompt_chat_gpt = """
            Reescreva o texto corrigindo os erros de escrita e ortografia e melhorando a escrita no geral.
            Ajustes os parágrafos, frases e palavras para melhorar a clareza e coesão do texto.
            Caso o texto não tenha erros, apenas reescreva-o de forma mais clara e coesa.
            Caso o texto apresente erros de escrita e ortografia, corrija-os.
            Caso o texto apresente problemas de coesão e clareza, ajuste-os.
            Caso o texto possua problemas de concordância, ajuste-os.
            Se o texto possuir algum tipo de formatação de texto, faça a reescrita ajustando também a formatação, para que o texto final tenha uma melhor apresentação.
            Texto a ser reescrito: '{texto}'.
            """

            # Gerando o prompt completo com a interpolação do texto no prompt base
            prompt_chat_gpt = prompt_chat_gpt.format(texto=texto)

            # Inferindo a reescrita do texto
            resultado, total_tokens = self.inferir(mensagem=prompt_chat_gpt)

            if resultado is None:
                raise Exception('Não foi possível inferir a reescrita do texto.')

            return resultado.replace("*", "").replace("#", "").strip(), total_tokens
        except Exception as ex:
            self.logs.error(f'Erro ao inferir a reescrita do texto: {ex}')
            raise ex
