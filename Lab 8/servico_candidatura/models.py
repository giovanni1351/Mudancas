from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class StatusCandidatura(str, Enum):
    PENDENTE = "PENDENTE"
    ACEITA = "ACEITA"
    REJEITADA = "REJEITADA"


class CandidaturaCreate(BaseModel):
    demanda_id: int = Field(..., description="ID da demanda de frete")
    caminhoneiro_id: int = Field(..., description="ID do caminhoneiro candidato")
    criador_demanda_id: int = Field(..., description="ID do criador da demanda (será notificado em eventos futuros)")
    mensagem: Optional[str] = Field(default=None, max_length=500, description="Mensagem de apresentação do caminhoneiro")


class CandidaturaResponse(BaseModel):
    id: int
    demanda_id: int
    caminhoneiro_id: int
    criador_demanda_id: int
    mensagem: Optional[str] = None
    status: StatusCandidatura
    criada_em: datetime
    atualizada_em: datetime

    model_config = {"from_attributes": True}
