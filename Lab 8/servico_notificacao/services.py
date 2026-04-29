from typing import List, Optional
from datetime import datetime, timezone

from .models import Notificacao, NotificacaoCreate


class NotificacaoService:
    """Lógica de negócio do Serviço de Notificação.

    Armazena notificações em memória. Em produção, seria substituído
    por persistência em banco de dados.
    """

    def __init__(self) -> None:
        self._db: dict[int, Notificacao] = {}
        self._counter: int = 0

    def criar(self, data: NotificacaoCreate) -> Notificacao:
        """Cria e persiste uma nova notificação."""
        self._counter += 1
        notificacao = Notificacao(
            id=self._counter,
            destinatario_id=data.destinatario_id,
            tipo=data.tipo,
            titulo=data.titulo,
            mensagem=data.mensagem,
            dados_extras=data.dados_extras,
            lida=False,
            criada_em=datetime.now(timezone.utc),
        )
        self._db[self._counter] = notificacao
        return notificacao

    def listar(self) -> List[Notificacao]:
        """Retorna todas as notificações registradas."""
        return list(self._db.values())

    def buscar_por_id(self, notificacao_id: int) -> Optional[Notificacao]:
        """Busca uma notificação pelo seu ID. Retorna None se não encontrada."""
        return self._db.get(notificacao_id)

    def listar_por_destinatario(self, destinatario_id: int) -> List[Notificacao]:
        """Retorna todas as notificações de um destinatário específico."""
        return [n for n in self._db.values() if n.destinatario_id == destinatario_id]
