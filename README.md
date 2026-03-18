# 🤖 Agent Support with LangGraph

Projeto de agente conversacional utilizando **LangGraph**, **LangChain**
e **OpenAI**, com execução em terminal e suporte a ferramentas (tools) e
memória simples de contexto.

------------------------------------------------------------------------

## 🚀 Visão Geral

Este projeto implementa um agente inteligente baseado em grafos de
estado (**StateGraph**) que:

-   Processa mensagens do usuário
-   Decide dinamicamente quando utilizar ferramentas
-   Executa funções externas (tools)
-   Mantém histórico da conversa (memória simples)
-   Retorna respostas contextualizadas

------------------------------------------------------------------------

## 🧠 Arquitetura

O fluxo do agente é estruturado com LangGraph:

    User Input → Agent Node → (Decision)
                            ↘ Tools Node → Agent Node → Final Response

### Componentes principais:

-   **Agent Node**
    -   Responsável por interpretar o contexto e decidir ações
-   **Tools Node**
    -   Executa ferramentas externas quando solicitado
-   **State (messages)**
    -   Mantém o histórico da conversa
-   **Conditional Edges**
    -   Controla o fluxo entre agent e tools

------------------------------------------------------------------------

## 🛠️ Tecnologias Utilizadas

-   Python
-   LangChain
-   LangGraph
-   OpenAI API
-   UV (gerenciamento de dependências)
-   dotenv

------------------------------------------------------------------------

## 💾 Memória do Agente

O agente mantém uma memória simples durante a execução:

-   Histórico contínuo da conversa
-   Contexto preservado entre interações
-   Sem uso de banco externo (in-memory)

------------------------------------------------------------------------

## ▶️ Como Executar

### 1. Clonar o repositório

    git clone https://github.com/MarcioLuizBR/agent-support-langgraph.git
    cd agent-support-langgraph

### 2. Criar ambiente com UV

    uv venv
    uv pip install -r requirements.txt

### 3. Configurar variáveis de ambiente

Crie um arquivo `.env`:

    OPENAI_API_KEY=your_api_key_here

### 4. Executar o projeto

    python main.py

------------------------------------------------------------------------

## 💬 Exemplo de Uso

    Você: Qual o status do serviço X?
    Agente: O serviço X está operacional.

O agente decide automaticamente quando usar tools.

------------------------------------------------------------------------

## 📦 Estrutura do Projeto

    ├── main.py
    ├── tools.py
    ├── pyproject.toml
    ├── uv.lock
    ├── .env
    └── README.md

------------------------------------------------------------------------

## 🎯 Objetivo do Projeto

Este projeto faz parte de um portfólio focado em:

-   Agentes inteligentes
-   Arquiteturas com LLMs
-   Integração de tools
-   Engenharia de contexto
-   Aplicações reais com LangGraph

------------------------------------------------------------------------

## 📈 Próximos Passos

-   Logs estruturados do fluxo do agente
-   Persistência de memória (arquivo ou banco)
-   Interface web (FastAPI ou Streamlit)
-   Deploy em ambiente cloud

------------------------------------------------------------------------

## 🤝 Contribuição

Sinta-se à vontade para abrir issues ou contribuir com melhorias.

------------------------------------------------------------------------

## 👤 Autor

**Márcio Luiz**\
[GitHub](https://github.com/MarcioLuizBR)\
[LinkedIn](https://www.linkedin.com/in/marcio-luiz/)

------------------------------------------------------------------------

## ⭐ Se este projeto te ajudou

Considere deixar uma estrela ⭐ no repositório!
