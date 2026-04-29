from fastapi import APIRouter, HTTPException, Depends
from typing import List

from .models import Notificacao, NotificacaoCreate
from .services import NotificacaoService

router = APIRouter(prefix="/notificacoes", tags=["Notificações"])

# Singleton padrão para uso em produção
_default_service = NotificacaoService()


def get_service() -> NotificacaoService:
    """Provedor de dependência — permite override nos testes."""
    return _default_service


@router.post(
    "/",
    response_model=Notificacao,
    status_code=201,
    summary="Criar notificação",
    description="Recebe e armazena uma nova notificação. Chamado pelo Serviço de Candidatura (orquestrador).",
)
def criar_notificacao(
    data: NotificacaoCreate,
    service: NotificacaoService = Depends(get_service),
) -> Notificacao:
    return service.criar(data)


@router.get(
    "/",
    response_model=List[Notificacao],
    summary="Listar todas as notificações",
)
def listar_notificacoes(
    service: NotificacaoService = Depends(get_service),
) -> List[Notificacao]:
    return service.listar()


@router.get(
    "/destinatario/{destinatario_id}",
    response_model=List[Notificacao],
    summary="Listar notificações por destinatário",
)
def listar_por_destinatario(
    destinatario_id: int,
    service: NotificacaoService = Depends(get_service),
) -> List[Notificacao]:
    return service.listar_por_destinatario(destinatario_id)


@router.get(
    "/{notificacao_id}",
    response_model=Notificacao,
    summary="Buscar notificação por ID",
)
def buscar_notificacao(
    notificacao_id: int,
    service: NotificacaoService = Depends(get_service),
) -> Notificacao:
    notificacao = service.buscar_por_id(notificacao_id)
    if not notificacao:
        raise HTTPException(status_code=404, detail="Notificação não encontrada")
    return notificacao
