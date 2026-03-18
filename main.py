import os
from typing import TypedDict, Annotated

from dotenv import load_dotenv

# Importa o modelo de chat da OpenAI via LangChain
from langchain_openai import ChatOpenAI

# Importa os tipos de mensagens estruturadas
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    ToolMessage,
    BaseMessage
)

# Importa utilitário para acumular mensagens no estado
from langgraph.graph.message import add_messages

# Importa os componentes principais do LangGraph
from langgraph.graph import StateGraph, END

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


# Define a estrutura do estado compartilhado no grafo
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def agent_node(state: AgentState) -> AgentState:
    """
    Nó principal do agente.
    Recebe as mensagens acumuladas no estado e chama o modelo.
    """
    system_message = SystemMessage(
        content=(
            "Você é um assistente técnico especializado em suporte. "
            "Quando o usuário perguntar sobre o status de um serviço, "
            "utilize a tool disponível."
        )
    )

    # Invoca o modelo com a mensagem de sistema + histórico do estado
    response = llm_with_tools.invoke([system_message] + state["messages"])

    # Retorna a nova resposta para ser anexada ao estado
    return {"messages": [response]}


def should_continue(state: AgentState) -> str:
    """
    Decide o próximo passo do fluxo.
    Se houver tool_calls, vai para o nó de tools.
    Caso contrário, encerra o fluxo.
    """
    last_message = state["messages"][-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    return "end"


def tools_node(state: AgentState) -> AgentState:
    """
    Executa as tools solicitadas pelo modelo e devolve os resultados
    como ToolMessage para o estado.
    """
    last_message = state["messages"][-1]
    tool_messages = []

    # Percorre todas as tool calls solicitadas pelo modelo
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        # Seleciona e executa a tool correspondente
        selected_tool = tool_map[tool_name]
        result = selected_tool.invoke(tool_args)

        # Adiciona o resultado como ToolMessage
        tool_messages.append(
            ToolMessage(
                content=result,
                tool_call_id=tool_call["id"]
            )
        )

    return {"messages": tool_messages}


def build_graph():
    """
    Monta e compila o grafo do agente.
    """
    graph = StateGraph(AgentState)

    # Adiciona os nós do fluxo
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tools_node)

    # Define o ponto de entrada
    graph.set_entry_point("agent")

    # Define a transição condicional após o nó do agente
    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END
        }
    )

    # Após executar tools, volta para o agente
    graph.add_edge("tools", "agent")

    return graph.compile()


def main():
    # Compila o app do LangGraph
    app = build_graph()

    print("Agente com LangGraph iniciado. Digite 'sair' para encerrar.\n")

    while True:
        # Captura a entrada do usuário
        user_input = input("Você: ")

        # Condição de saída do programa
        if user_input.lower() in ["sair", "exit", "quit"]:
            print("Encerrando agente.")
            break

        # Inicia o estado com a mensagem do usuário
        initial_state = {
            "messages": [HumanMessage(content=user_input)]
        }

        # Executa o grafo
        result = app.invoke(initial_state)

        # Obtém a última mensagem gerada
        final_message = result["messages"][-1]

        print("\nAgente:")
        print(final_message.content)
        print()


# Ponto de entrada do programa
if __name__ == "__main__":
    main()