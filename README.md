# 🤖 Agent Support com LangGraph

> Agente conversacional com **LangGraph + LangChain + OpenAI**, com controle de fluxo, execução de tools, memória de sessão e observabilidade via logs.  
>  
> Projeto estruturado com foco em **Agent Engineering** e pronto para evoluções reais (API, persistência, UI e deploy).

---

## 🚀 Visão Geral

Este projeto demonstra a construção de um **agente baseado em grafos (LangGraph)**, indo além de um chat simples.

A arquitetura implementa:

- Orquestração de fluxo com `StateGraph`
- Decisão dinâmica de uso de ferramentas (tool calling)
- Execução de funções externas
- Loop de raciocínio (agent ↔ tools)
- Memória de sessão (histórico contínuo)
- Logs estruturados para rastreabilidade

💡 O objetivo é simular um **agente de suporte técnico**, com comportamento controlado e extensível.

---

## 🧠 Arquitetura do Agente

```text
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
```

### 🔹 Componentes principais

**Agent Node**
- Interage com o modelo LLM
- Recebe histórico completo
- Decide quando usar tools

**Tools Node**
- Executa funções externas
- Retorna `ToolMessage` para o fluxo

**State (messages)**
- Armazena todo o histórico da conversa
- Base da memória do agente

**Conditional Edge**
- Controla o fluxo entre agent → tools → agent ou finalização

---

## 🧠 Memória de Sessão

- Histórico contínuo durante a execução
- Preserva contexto entre interações
- Implementação em memória (in-memory)
- Sem dependência de banco externo

👉 Ideal para MVP e evolução incremental

---

## 📊 Observabilidade (Logs)

O agente possui logs estruturados no terminal:

- Entrada no agent node
- Decisão de fluxo
- Execução de tools
- Argumentos utilizados
- Resultado das tools

👉 Facilita debug, entendimento do fluxo e evolução do sistema

---

## 🔧 Tecnologias

- Python
- LangChain
- LangGraph
- OpenAI API
- UV (dependency management)
- python-dotenv

---

## ⚙️ Como Rodar

### 1) Clone o repositório

```bash
git clone https://github.com/MarcioLuizBR/agent-support-langgraph.git
cd agent-support-langgraph
```

### 2) Ambiente virtual (UV)

```bash
uv venv
uv pip install -r requirements.txt
```

### 3) Variáveis de ambiente

Crie um arquivo `.env`:

```env
OPENAI_API_KEY=your_api_key_here
```

### 4) Executar o agente

```bash
python main.py
```

---

## 💬 Exemplos de Uso

```text
Você: Meu nome é Márcio
Agente: Prazer, Márcio!

Você: Qual é o meu nome?
Agente: Seu nome é Márcio.

Você: Qual o status do serviço api?
Agente: A API principal está estável e sem incidentes no momento.
```

---

## 🧩 Estrutura do Projeto

```text
├── main.py              # Orquestração do grafo + loop CLI
├── tools.py             # Definição das tools
├── pyproject.toml       # Configuração do projeto
├── uv.lock              # Lock de dependências
└── README.md
```

---

## ⭐ Diferenciais

- Uso real de **LangGraph (StateGraph)**
- Arquitetura baseada em fluxo (graph-based agent)
- Execução dinâmica de tools (tool calling)
- Loop agent ↔ tools
- Memória de contexto funcional
- Logs estruturados (observabilidade)
- Base pronta para evolução para produção

---

## 📈 Roadmap

- [x] Memória de sessão
- [x] Logs estruturados
- [ ] Persistência de memória (arquivo / DB / vector store)
- [ ] API (FastAPI)
- [ ] Interface web (Streamlit)
- [ ] Deploy (Azure / AWS)
- [ ] Monitoramento e tracing

---

## 🎯 Propósito

Projeto desenvolvido como parte de portfólio com foco em:

- Agent Engineering
- Arquiteturas com LLMs
- Integração com ferramentas externas
- Controle de fluxo com grafos (LangGraph)

---

## 👤 Autor

**Márcio Luiz**

- GitHub: https://github.com/MarcioLuizBR  
- LinkedIn: https://www.linkedin.com/in/marcioluiz-br/

---

## 🙌 Contribuição

Se este projeto te ajudou, considere deixar uma ⭐ no repositório.

---
