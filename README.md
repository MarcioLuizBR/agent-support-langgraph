# 🤖 Agent Support com LangGraph

> Um agente conversacional inteligente construído com **LangGraph +
> LangChain + OpenAI**, capaz de tomar decisões, executar ferramentas e
> manter contexto de conversa --- simulando arquiteturas reais de
> agentes modernos.

------------------------------------------------------------------------

## 🚀 Visão Geral

Este projeto implementa um agente baseado em **StateGraph (LangGraph)**
que:

-   Interpreta mensagens do usuário
-   Decide dinamicamente quando usar ferramentas (tools)
-   Executa funções externas
-   Mantém histórico da conversa (memória simples)
-   Responde de forma contextual e iterativa

👉 O objetivo é simular um **agente real de produção**, com fluxo
controlado, separação de responsabilidades e arquitetura escalável.

------------------------------------------------------------------------

## 🧠 Arquitetura do Agente

    User Input
        ↓
    [ Agent Node ]
        ↓ (decisão)
     ┌───────────────┐
     │               │
     ▼               ▼
    END         [ Tools Node ]
                    ↓
               [ Agent Node ]

------------------------------------------------------------------------

### 🔹 Componentes principais

#### 1. Agent Node

Responsável por interpretar o contexto, decidir ações e gerar respostas.

#### 2. Tools Node

Executa funções externas e retorna resultados estruturados
(`ToolMessage`).

#### 3. Estado (State)

``` python
messages: List[BaseMessage]
```

Armazena todo o histórico da conversa.

#### 4. Controle de fluxo

-   `should_continue()` decide o próximo passo
-   Permite loop entre agente ↔ tools

------------------------------------------------------------------------

## 🧠 Memória do Agente

-   Histórico contínuo da conversa
-   Contexto preservado entre interações
-   Armazenamento em memória (in-memory)

------------------------------------------------------------------------

## 🛠️ Tecnologias Utilizadas

-   Python
-   LangChain
-   LangGraph
-   OpenAI API
-   UV
-   dotenv

------------------------------------------------------------------------

## ⚙️ Como Executar

### 1. Clone o repositório

    git clone https://github.com/MarcioLuizBR/agent-support-langgraph.git
    cd agent-support-langgraph

### 2. Ambiente com UV

    uv venv
    uv pip install -r requirements.txt

### 3. .env

    OPENAI_API_KEY=your_api_key_here

### 4. Executar

    python main.py

------------------------------------------------------------------------

## 💬 Exemplo

    Você: Meu nome é Márcio
    Você: Qual é o meu nome?
    Você: Consulte o status do serviço X

------------------------------------------------------------------------

## 📂 Estrutura

    ├── main.py
    ├── tools.py
    ├── pyproject.toml
    ├── uv.lock
    └── README.md

------------------------------------------------------------------------

## 🎯 Objetivo

Projeto focado em:

-   Agent Engineering
-   LLMs na prática
-   Arquiteturas com LangGraph

------------------------------------------------------------------------

## 📈 Próximos passos

-   Logs do agente
-   Persistência de memória
-   API com FastAPI
-   Deploy cloud

------------------------------------------------------------------------

## 👤 Autor

Márcio Luiz\
https://github.com/MarcioLuizBR\
https://www.linkedin.com/in/marcio-luiz/

------------------------------------------------------------------------

## ⭐

Se ajudou, deixa uma estrela!
