# 🤖 Agent Support com LangGraph

> Agente conversacional com **LangGraph + LangChain + OpenAI**, com
> tomada de decisão, execução de ferramentas e memória de contexto ---
> arquitetura pronta para evoluir para produção.

------------------------------------------------------------------------

## 🚀 Visão Geral

Este projeto demonstra uma arquitetura moderna de **Agent Engineering**
usando **StateGraph (LangGraph)** para orquestrar:

-   Interpretação de mensagens do usuário
-   Decisão de uso de ferramentas (tool calling)
-   Execução de funções externas
-   Loop de raciocínio (agent ↔ tools)
-   Memória de sessão (histórico contínuo)

💡 Objetivo: sair do "chat simples" e construir um **agente
estruturado**, com separação de responsabilidades e fluxo controlado.

------------------------------------------------------------------------

## 🧠 Arquitetura (StateGraph)

    User Input
        ↓
    [ Agent Node ]
        ↓ (decision: tools?)
     ┌───────────────┐
     │               │
     ▼               ▼
    END         [ Tools Node ]
                    ↓
               [ Agent Node ]

### Componentes

-   **Agent Node**
    -   LLM + contexto
    -   Decide ações e quando chamar tools
-   **Tools Node**
    -   Executa funções externas
    -   Retorna `ToolMessage`
-   **State (messages)**
    -   Histórico completo da conversa
-   **Conditional Edge**
    -   Controla o fluxo (continua ou encerra)

------------------------------------------------------------------------

## 🧠 Memória (Session Memory)

-   Histórico contínuo durante a execução
-   Preserva contexto entre interações
-   Implementação simples (in-memory)
-   Sem banco externo (ideal para MVP)

------------------------------------------------------------------------

## 🔧 Tecnologias

-   Python
-   LangChain
-   LangGraph
-   OpenAI API
-   UV (dependency management)
-   python-dotenv

------------------------------------------------------------------------

## ⚙️ Como Rodar

### 1) Clone

    git clone https://github.com/MarcioLuizBR/agent-support-langgraph.git
    cd agent-support-langgraph

### 2) Ambiente (UV)

    uv venv
    uv pip install -r requirements.txt

### 3) Variáveis de ambiente

Crie `.env`:

    OPENAI_API_KEY=your_api_key_here

### 4) Executar

    python main.py

------------------------------------------------------------------------

## 💬 Exemplo

    Você: Meu nome é Márcio
    Agente: Prazer, Márcio!

    Você: Qual é o meu nome?
    Agente: Seu nome é Márcio.

    Você: Consulte o status do serviço X
    Agente: O serviço X está operacional.

------------------------------------------------------------------------

## 🧩 Estrutura

    ├── main.py              # Orquestração do grafo + loop CLI
    ├── tools.py             # Definição das tools
    ├── pyproject.toml       # Config do projeto
    ├── uv.lock              # Lock de dependências
    └── README.md

------------------------------------------------------------------------

## ⭐ Diferenciais

-   Uso real de **LangGraph (StateGraph)**
-   **Tool calling** com retorno estruturado
-   Loop agent ↔ tools
-   **Memória de contexto** funcional
-   Base pronta para evolução (logs, API, persistência)

------------------------------------------------------------------------

## 📈 Roadmap

-   [ ] Logs estruturados do fluxo
-   [ ] Persistência de memória (arquivo / DB / vector store)
-   [ ] API (FastAPI)
-   [ ] UI (Streamlit)
-   [ ] Deploy (Azure/AWS)
-   [ ] Observabilidade

------------------------------------------------------------------------

## 🎯 Propósito

Portfólio focado em: - Agent Engineering - Arquiteturas com LLMs -
Integração com ferramentas - Controle de fluxo com grafos

------------------------------------------------------------------------

## 👤 Autor

Márcio Luiz\
GitHub: https://github.com/MarcioLuizBR/
LinkedIn: https://www.linkedin.com/in/marcioluiz-br/

------------------------------------------------------------------------

## 🙌 Se te ajudou

Deixe uma ⭐ no repositório!
