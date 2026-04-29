import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from .models import CandidaturaCreate, CandidaturaResponse
from .orquestrador import notificar_status_candidatura
from .services import CandidaturaService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/candidaturas", tags=["Candidaturas"])

# Singleton padrão para uso em produção
_default_service = CandidaturaService()


def get_service() -> CandidaturaService:
    """Provedor de dependência — permite override nos testes."""
    return _default_service


@router.post(
    "/",
    response_model=CandidaturaResponse,
    status_code=201,
    summary="Criar candidatura",
    description="Registra a candidatura de um caminhoneiro a uma demanda de frete.",
)
async def criar_candidatura(
    data: CandidaturaCreate,
    service: CandidaturaService = Depends(get_service),
) -> CandidaturaResponse:
    return service.criar(data)


@router.get(
    "/",
    response_model=List[CandidaturaResponse],
    summary="Listar candidaturas",
)
async def listar_candidaturas(
    service: CandidaturaService = Depends(get_service),
) -> List[CandidaturaResponse]:
    return service.listar()


@router.get(
    "/{candidatura_id}",
    response_model=CandidaturaResponse,
    summary="Buscar candidatura por ID",
)
async def buscar_candidatura(
    candidatura_id: int,
    service: CandidaturaService = Depends(get_service),
) -> CandidaturaResponse:
    candidatura = service.buscar_por_id(candidatura_id)
    if not candidatura:
        raise HTTPException(status_code=404, detail="Candidatura não encontrada")
    return candidatura


@router.patch(
    "/{candidatura_id}/aceitar",
    response_model=CandidaturaResponse,
    summary="Aceitar candidatura",
    description=(
        "Aceita uma candidatura PENDENTE e, via **orquestração**, "
        "dispara uma notificação ao caminhoneiro pelo Serviço de Notificação."
    ),
)
async def aceitar_candidatura(
    candidatura_id: int,
    service: CandidaturaService = Depends(get_service),
) -> CandidaturaResponse:
    try:
        candidatura = service.aceitar(candidatura_id)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    if not candidatura:
        raise HTTPException(status_code=404, detail="Candidatura não encontrada")
    await notificar_status_candidatura(candidatura)
    return candidatura


@router.patch(
    "/{candidatura_id}/rejeitar",
    response_model=CandidaturaResponse,
    summary="Rejeitar candidatura",
    description=(
        "Rejeita uma candidatura PENDENTE e, via **orquestração**, "
        "dispara uma notificação ao caminhoneiro pelo Serviço de Notificação."
    ),
)
async def rejeitar_candidatura(
    candidatura_id: int,
    service: CandidaturaService = Depends(get_service),
) -> CandidaturaResponse:
    try:
        candidatura = service.rejeitar(candidatura_id)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    if not candidatura:
        raise HTTPException(status_code=404, detail="Candidatura não encontrada")
    await notificar_status_candidatura(candidatura)
    return candidatura
