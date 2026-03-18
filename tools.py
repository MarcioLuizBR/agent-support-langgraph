# Importa o decorator para transformar uma função em tool
from langchain_core.tools import tool


@tool
def consultar_status_servico(servico: str) -> str:
    """
    Consulta o status de um serviço interno.
    Use esta tool quando o usuário perguntar sobre o status de algum serviço.
    """

    # Base simulada de status dos serviços, fake para fins de demonstração
    status_fake = {
        "api": "A API principal está estável e sem incidentes no momento.",
        "banco de dados": "O banco de dados está operacional e com desempenho normal.",
        "agente": "O agente em produção está funcionando normalmente.",
        "servidor": "O servidor está online, sem alertas críticos."
    }

    # Padroniza o texto recebido
    servico_normalizado = servico.strip().lower()

    # Retorna o status encontrado ou uma mensagem padrão
    return status_fake.get(
        servico_normalizado,
        f"Não encontrei informações sobre o serviço '{servico}'."
    )