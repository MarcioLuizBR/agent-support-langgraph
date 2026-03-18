import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# Importa a tool criada no arquivo tools.py
from tools import consultar_status_servico


# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Recupera a chave da OpenAI
api_key = os.getenv("OPENAI_API_KEY")

# Validação simples para garantir que a chave existe
if not api_key:
    raise ValueError("A variável OPENAI_API_KEY não foi encontrada no arquivo .env")

# Lista de tools disponíveis
tools = [consultar_status_servico]

# Mapeia o nome da tool para a função correspondente
tool_map = {
    consultar_status_servico.name: consultar_status_servico
}

# Inicializa o modelo de linguagem
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=api_key
)

# Vincula as tools ao modelo
llm_with_tools = llm.bind_tools(tools=tools)


def main():
    # Define o contexto do agente (comportamento)
    system_message = SystemMessage(
        content=(
            "Você é um assistente técnico especializado em suporte. "
            "Quando o usuário perguntar sobre o status de um serviço, "
            "utilize a tool disponível."
        )
    )

    print("Agente iniciado. Digite 'sair' para encerrar.\n")

    while True:
        # Captura a pergunta do usuário
        user_input = input("Você: ")

        # Condição de saída do programa
        if user_input.lower() in ["sair", "exit", "quit"]:
            print("Encerrando agente.")
            break

        # Cria a mensagem do usuário
        user_message = HumanMessage(content=user_input)

        # Monta a lista de mensagens enviada ao modelo
        mensagens = [system_message, user_message]

        # Invoca o modelo com suporte a tools
        resposta = llm_with_tools.invoke(mensagens)

        # Verifica se o modelo decidiu usar alguma tool
        if resposta.tool_calls:
            # Captura a primeira tool chamada pelo modelo
            tool_call = resposta.tool_calls[0]

            # Extrai o nome da tool e seus argumentos
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            # Seleciona a função correspondente no mapa de tools
            selected_tool = tool_map[tool_name]

            # Executa a tool com os argumentos recebidos
            resultado_tool = selected_tool.invoke(tool_args)

            # Exibe o resultado da tool para o usuário
            print("\nAgente:")
            print(resultado_tool)
            print()

        else:
            # Caso o modelo não use tool, exibe a resposta normal
            print("\nAgente:")
            print(resposta.content)
            print()


# Ponto de entrada do programa
if __name__ == "__main__":
    main()