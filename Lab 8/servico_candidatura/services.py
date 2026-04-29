from typing import List, Optional
from datetime import datetime, timezone

from .models import CandidaturaCreate, CandidaturaResponse, StatusCandidatura


class CandidaturaService:
    """Lógica de negócio do Serviço de Candidatura.

    Gerencia o ciclo de vida das candidaturas: criação, consulta, aceitação
    e rejeição. Armazena em memória — em produção seria substituído por
    persistência em banco de dados.
    """

    def __init__(self) -> None:
        self._db: dict[int, CandidaturaResponse] = {}
        self._counter: int = 0

    def criar(self, data: CandidaturaCreate) -> CandidaturaResponse:
        """Registra uma nova candidatura com status PENDENTE."""
        self._counter += 1
        agora = datetime.now(timezone.utc)
        candidatura = CandidaturaResponse(
            id=self._counter,
            demanda_id=data.demanda_id,
            caminhoneiro_id=data.caminhoneiro_id,
            criador_demanda_id=data.criador_demanda_id,
            mensagem=data.mensagem,
            status=StatusCandidatura.PENDENTE,
            criada_em=agora,
            atualizada_em=agora,
        )
        self._db[self._counter] = candidatura
        return candidatura

    def listar(self) -> List[CandidaturaResponse]:
        """Retorna todas as candidaturas registradas."""
        return list(self._db.values())

    def buscar_por_id(self, candidatura_id: int) -> Optional[CandidaturaResponse]:
        """Busca uma candidatura pelo ID. Retorna None se não encontrada."""
        return self._db.get(candidatura_id)

    def aceitar(self, candidatura_id: int) -> Optional[CandidaturaResponse]:
        """Aceita uma candidatura PENDENTE.

        Raises:
            ValueError: se a candidatura já foi processada anteriormente.
        Returns:
            CandidaturaResponse atualizada, ou None se não encontrada.
        """
        candidatura = self._db.get(candidatura_id)
        if candidatura is None:
            return None
        if candidatura.status != StatusCandidatura.PENDENTE:
            raise ValueError(
                f"Candidatura já processada com status '{candidatura.status.value}'"
            )
        candidatura.status = StatusCandidatura.ACEITA
        candidatura.atualizada_em = datetime.now(timezone.utc)
        return candidatura

    def rejeitar(self, candidatura_id: int) -> Optional[CandidaturaResponse]:
        """Rejeita uma candidatura PENDENTE.

        Raises:
            ValueError: se a candidatura já foi processada anteriormente.
        Returns:
            CandidaturaResponse atualizada, ou None se não encontrada.
        """
        candidatura = self._db.get(candidatura_id)
        if candidatura is None:
            return None
        if candidatura.status != StatusCandidatura.PENDENTE:
            raise ValueError(
                f"Candidatura já processada com status '{candidatura.status.value}'"
            )
        candidatura.status = StatusCandidatura.REJEITADA
        candidatura.atualizada_em = datetime.now(timezone.utc)
        return candidatura
