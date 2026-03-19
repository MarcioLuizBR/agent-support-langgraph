import os
from datetime import datetime
from typing import TypedDict, Annotated

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    ToolMessage,
    BaseMessage,
)
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END

from tools import consultar_status_servico


# ================================
# 🔐 CONFIGURAÇÃO DE AMBIENTE
# ================================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("A variável OPENAI_API_KEY não foi encontrada no arquivo .env")


# ================================
# ⚙️ CONFIGURAÇÃO DE LOG
# ================================

LOG_ENABLED = False  # 👉 True = mostra logs | False = saída limpa (para print)


def log_step(message: str):
    """
    Log simples controlado por flag.
    """
    if not LOG_ENABLED:
        return

    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [LOG] {message}")


# ================================
# 🧰 TOOLS
# ================================

tools = [consultar_status_servico]

tool_map = {
    consultar_status_servico.name: consultar_status_servico
}


# ================================
# 🤖 MODELO
# ================================

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=api_key
)

llm_with_tools = llm.bind_tools(tools=tools)


# ================================
# 🧠 ESTADO
# ================================

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# ================================
# 🧠 NODE: AGENT
# ================================

def agent_node(state: AgentState) -> AgentState:
    log_step("Entrando em agent_node")
    log_step(f"Mensagens no estado: {len(state['messages'])}")

    system_message = SystemMessage(
        content=(
            "Você é um assistente técnico especializado em suporte. "
            "Quando o usuário perguntar sobre o status de um serviço, "
            "utilize a tool disponível."
        )
    )

    response = llm_with_tools.invoke([system_message] + state["messages"])

    if hasattr(response, "tool_calls") and response.tool_calls:
        tool_names = [tool_call["name"] for tool_call in response.tool_calls]
        log_step(f"Modelo solicitou tool(s): {tool_names}")
    else:
        log_step("Modelo respondeu sem usar tools")

    return {"messages": [response]}


# ================================
# 🔀 DECISÃO
# ================================

def should_continue(state: AgentState) -> str:
    log_step("Avaliando fluxo (should_continue)")

    last_message = state["messages"][-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        log_step("→ indo para tools")
        return "tools"

    log_step("→ finalizando fluxo")
    return "end"


# ================================
# 🔧 NODE: TOOLS
# ================================

def tools_node(state: AgentState) -> AgentState:
    log_step("Entrando em tools_node")

    last_message = state["messages"][-1]
    tool_messages = []

    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        log_step(f"Executando tool: {tool_name}")
        log_step(f"Argumentos: {tool_args}")

        selected_tool = tool_map[tool_name]
        result = selected_tool.invoke(tool_args)

        log_step(f"Resultado: {result}")

        tool_messages.append(
            ToolMessage(
                content=result,
                tool_call_id=tool_call["id"]
            )
        )

    log_step("Finalizando tools_node")

    return {"messages": tool_messages}


# ================================
# 🧱 GRAFO
# ================================

def build_graph():
    log_step("Construindo grafo")

    graph = StateGraph(AgentState)

    graph.add_node("agent", agent_node)
    graph.add_node("tools", tools_node)

    graph.set_entry_point("agent")

    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END
        }
    )

    graph.add_edge("tools", "agent")

    log_step("Grafo pronto")

    return graph.compile()


# ================================
# 🚀 MAIN
# ================================

def main():
    app = build_graph()

    conversation_history = []

    print("Agente iniciado.")
    print("Digite 'sair' para encerrar.\n")

    while True:
        user_input = input("Você: ")

        if user_input.lower() in ["sair", "exit", "quit"]:
            print("Encerrando.")
            break

        log_step(f"Input usuário: {user_input}")

        # adiciona ao histórico
        conversation_history.append(HumanMessage(content=user_input))

        # executa o grafo
        result = app.invoke({
            "messages": conversation_history
        })

        # atualiza memória
        conversation_history = result["messages"]

        final_message = conversation_history[-1]

        log_step("Resposta pronta")

        print("\nAgente:")
        print(final_message.content)
        print()


if __name__ == "__main__":
    main()