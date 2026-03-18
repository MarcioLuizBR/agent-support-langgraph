import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Recupera a chave da OpenAI
api_key = os.getenv("OPENAI_API_KEY")

# Validação simples para garantir que a chave existe
if not api_key:
    raise ValueError("A variável OPENAI_API_KEY não foi encontrada no arquivo .env")

llm = ChatOpenAI(
    model="gpt-4o-mini", 
    temperature=0, 
    api_key=api_key
    )

def main():
    # Define o contexto do agente (comportamento)
    system_message = SystemMessage(
        content="Você é um assistente técnico especializado em suporte."
    )

    # Define a pergunta do usuário
    user_message = HumanMessage(
        content="Qual a função de um agente de IA?"
    )

    # Junta as mensagens em uma lista (estrutura de chat)
    mensagens = [system_message, user_message]

    resposta = llm.invoke(mensagens)

    print("\nResposta do agente:\n")
    print(resposta.content)


if __name__ == "__main__":
    main()