import os
from datetime import datetime
from typing import TypedDict, Annotated

from dotenv import load_dotenv

# Modelo de chat da OpenAI via LangChain
from langchain_openai import ChatOpenAI

# Tipos de mensagens estruturadas
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    ToolMessage,
    BaseMessage,
)

# Utilitário para acumular mensagens no estado do LangGraph
from langgraph.graph.message import add_messages

# Componentes principais do grafo
from langgraph.graph import StateGraph, END

# Tool customizada do projeto
from tools import consultar_status_servico


# ================================
# 🔐 CONFIGURAÇÃO DE AMBIENTE
# ================================

# Carrega variáveis do arquivo .env
load_dotenv()

# Recupera chave da OpenAI
api_key = os.getenv("OPENAI_API_KEY")

# Validação básica
if not api_key:
    raise ValueError("A variável OPENAI_API_KEY não foi encontrada no arquivo .env")


# ================================
# 🧰 CONFIGURAÇÃO DE TOOLS
# ================================

# Lista de tools disponíveis para o agente
tools = [consultar_status_servico]

# Mapeamento nome → função (necessário para execução dinâmica)
tool_map = {
    consultar_status_servico.name: consultar_status_servico
}


# ================================
# 🤖 CONFIGURAÇÃO DO MODELO
# ================================

# Inicializa o modelo LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=api_key
)

# Habilita uso de tools no modelo
llm_with_tools = llm.bind_tools(tools=tools)


# ================================
# 🧠 ESTRUTURA DE ESTADO
# ================================

class AgentState(TypedDict):
    """
    Define o estado compartilhado do grafo.

    - messages: lista acumulada de mensagens (histórico da conversa)
    - add_messages: garante que novas mensagens sejam anexadas automaticamente
    """
    messages: Annotated[list[BaseMessage], add_messages]


# ================================
# 📊 LOG SIMPLES
# ================================

def log_step(message: str):
    """
    Função auxiliar para logs estruturados no terminal.

    Mantém padrão visual e adiciona timestamp para rastreabilidade.
    """
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [LOG] {message}")


# ================================
# 🧠 NÓ: AGENT
# ================================

def agent_node(state: AgentState) -> AgentState:
    """
    Nó principal do agente.

    Responsável por:
    - Receber o estado atual (histórico de mensagens)
    - Chamar o modelo LLM
    - Decidir (implicitamente) se precisa usar tools
    """

    log_step("Entrando em agent_node")
    log_step(f"Quantidade de mensagens no estado: {len(state['messages'])}")

    # Prompt de sistema define o comportamento do agente
    system_message = SystemMessage(
        content=(
            "Você é um assistente técnico especializado em suporte. "
            "Quando o usuário perguntar sobre o status de um serviço, "
            "utilize a tool disponível."
        )
    )

    # Chamada ao modelo com histórico completo
    response = llm_with_tools.invoke([system_message] + state["messages"])

    # Log para identificar decisão do modelo
    if hasattr(response, "tool_calls") and response.tool_calls:
        tool_names = [tool_call["name"] for tool_call in response.tool_calls]
        log_step(f"Modelo solicitou tool(s): {tool_names}")
    else:
        log_step("Modelo respondeu sem solicitar tools")

    # Retorna nova mensagem para ser anexada ao estado
    return {"messages": [response]}


# ================================
# 🔀 DECISÃO DE FLUXO
# ================================

def should_continue(state: AgentState) -> str:
    """
    Define o roteamento do grafo.

    - Se houver tool_calls → vai para 'tools'
    - Caso contrário → encerra fluxo
    """

    log_step("Avaliando transição em should_continue")

    last_message = state["messages"][-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        log_step("Decisão do fluxo: ir para tools")
        return "tools"

    log_step("Decisão do fluxo: encerrar")
    return "end"


# ================================
# 🔧 NÓ: TOOLS
# ================================

def tools_node(state: AgentState) -> AgentState:
    """
    Executa tools solicitadas pelo modelo.

    Fluxo:
    - Lê tool_calls da última mensagem
    - Executa cada tool
    - Retorna resultados como ToolMessage
    """

    log_step("Entrando em tools_node")

    last_message = state["messages"][-1]
    tool_messages = []

    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        log_step(f"Executando tool: {tool_name}")
        log_step(f"Argumentos da tool: {tool_args}")

        # Executa a tool correspondente
        selected_tool = tool_map[tool_name]
        result = selected_tool.invoke(tool_args)

        log_step(f"Resultado da tool '{tool_name}': {result}")

        # Encapsula resultado no formato esperado pelo LangGraph
        tool_messages.append(
            ToolMessage(
                content=result,
                tool_call_id=tool_call["id"]
            )
        )

    log_step("Finalizando tools_node e retornando mensagens ao grafo")

    return {"messages": tool_messages}


# ================================
# 🧱 CONSTRUÇÃO DO GRAFO
# ================================

def build_graph():
    """
    Monta e compila o grafo do agente.
    """

    log_step("Construindo grafo do agente")

    graph = StateGraph(AgentState)

    # Define nós
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tools_node)

    # Define entrada
    graph.set_entry_point("agent")

    # Define decisão condicional
    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END
        }
    )

    # Loop de retorno após execução de tools
    graph.add_edge("tools", "agent")

    log_step("Grafo compilado com sucesso")

    return graph.compile()


# ================================
# 🚀 LOOP PRINCIPAL (TERMINAL)
# ================================

def main():
    """
    Loop interativo do agente no terminal.

    Responsável por:
    - Capturar entrada do usuário
    - Manter histórico (memória simples)
    - Executar o grafo
    - Exibir resposta
    """

    app = build_graph()

    # Memória em tempo de execução (sem persistência externa)
    conversation_history = []

    print("Agente com memória simples iniciado.")
    print("Digite 'sair' para encerrar.\n")

    while True:
        user_input = input("Você: ")

        # Condição de saída
        if user_input.lower() in ["sair", "exit", "quit"]:
            print("Encerrando agente.")
            break

        log_step(f"Nova entrada do usuário: {user_input}")

        # Adiciona nova mensagem ao histórico
        conversation_history.append(HumanMessage(content=user_input))

        # Executa o grafo com todo o histórico acumulado
        result = app.invoke({
            "messages": conversation_history
        })

        # Atualiza memória com estado retornado
        conversation_history = result["messages"]

        # Última mensagem = resposta final
        final_message = conversation_history[-1]

        log_step("Resposta final pronta para exibição")

        print("\nAgente:")
        print(final_message.content)
        print()


# ================================
# ▶️ ENTRYPOINT
# ================================

if __name__ == "__main__":
    main()