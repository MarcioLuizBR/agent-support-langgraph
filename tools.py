from langchain_core.tools import tool


@tool
def consultar_status_servico(servico: str) -> str:
    """
    Consulta o status de um serviço interno.

    Use esta tool quando o usuário perguntar sobre o status de algum serviço.
    """

    # Base simulada de status dos serviços (mock)
    status_fake = {
        "api": "A API principal está estável e sem incidentes no momento.",
        "banco de dados": "O banco de dados está operacional e com desempenho normal.",
        "agente": "O agente em produção está funcionando normalmente.",
        "servidor": "O servidor está online, sem alertas críticos."
    }

    # Normaliza entrada (remove espaços e padroniza caixa)
    servico_normalizado = servico.strip().lower()

    # Caso o serviço exista
    if servico_normalizado in status_fake:
        return status_fake[servico_normalizado]

    # Caso não exista → resposta mais inteligente
    servicos_disponiveis = ", ".join(status_fake.keys())

    return (
        f"Não encontrei informações sobre o serviço '{servico}'. "
        f"Serviços disponíveis: {servicos_disponiveis}."
    )