"""Módulo de orquestração do Serviço de Candidatura.

Responsável por coordenar a comunicação com o Serviço de Notificação
após mudanças de status em candidaturas.

Padrão adotado: ORQUESTRAÇÃO
  - Este serviço (Candidatura) conhece o Serviço de Notificação e o chama
    ativamente via HTTP sempre que uma candidatura é aceita ou rejeitada.
  - A URL do Serviço de Notificação é configurável via variável de ambiente
    NOTIFICACAO_URL, garantindo portabilidade entre ambientes.
"""

import logging
import os

import httpx

from .models import CandidaturaResponse, StatusCandidatura

logger = logging.getLogger(__name__)

NOTIFICACAO_URL = os.getenv("NOTIFICACAO_URL", "http://localhost:8001")


def _montar_payload(candidatura: CandidaturaResponse) -> dict:
    """Constrói o payload de notificação de acordo com o status da candidatura."""
    if candidatura.status == StatusCandidatura.ACEITA:
        return {
            "destinatario_id": candidatura.caminhoneiro_id,
            "tipo": "CANDIDATURA_ACEITA",
            "titulo": "Candidatura aceita!",
            "mensagem": (
                f"Parabéns! Sua candidatura para a demanda #{candidatura.demanda_id} "
                "foi aceita. Entre em contato com o solicitante."
            ),
            "dados_extras": {
                "candidatura_id": candidatura.id,
                "demanda_id": candidatura.demanda_id,
                "criador_demanda_id": candidatura.criador_demanda_id,
            },
        }
    return {
        "destinatario_id": candidatura.caminhoneiro_id,
        "tipo": "CANDIDATURA_REJEITADA",
        "titulo": "Candidatura não selecionada",
        "mensagem": (
            f"Sua candidatura para a demanda #{candidatura.demanda_id} "
            "não foi selecionada desta vez. Continue tentando!"
        ),
        "dados_extras": {
            "candidatura_id": candidatura.id,
            "demanda_id": candidatura.demanda_id,
        },
    }


async def notificar_status_candidatura(
    candidatura: CandidaturaResponse,
    client: httpx.AsyncClient | None = None,
) -> dict:
    """Envia notificação ao Serviço de Notificação sobre mudança de status.

    Args:
        candidatura: Candidatura com o novo status (ACEITA ou REJEITADA).
        client: Cliente HTTP opcional — usado nos testes para injetar transporte ASGI.

    Returns:
        Dicionário com a notificação criada retornada pelo Serviço de Notificação.

    Raises:
        httpx.HTTPError: se o Serviço de Notificação retornar erro ou estiver indisponível.
    """
    payload = _montar_payload(candidatura)
    _owns_client = client is None
    _client = client or httpx.AsyncClient(base_url=NOTIFICACAO_URL, timeout=5.0)

    try:
        response = await _client.post("/notificacoes/", json=payload)
        response.raise_for_status()
        logger.info(
            "Notificação enviada — candidatura_id=%s status=%s",
            candidatura.id,
            candidatura.status.value,
        )
        return response.json()
    except httpx.HTTPError as exc:
        logger.error("Falha ao notificar serviço de notificação: %s", exc)
        raise
    finally:
        if _owns_client:
            await _client.aclose()
