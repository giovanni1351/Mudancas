from pydantic import BaseModel, Field
from typing import Optional, Any, Dict
from datetime import datetime
from enum import Enum


class TipoNotificacao(str, Enum):
    CANDIDATURA_ACEITA = "CANDIDATURA_ACEITA"
    CANDIDATURA_REJEITADA = "CANDIDATURA_REJEITADA"
    INFO = "INFO"


class NotificacaoCreate(BaseModel):
    destinatario_id: int = Field(..., description="ID do usuário destinatário")
    tipo: TipoNotificacao = Field(..., description="Tipo da notificação")
    titulo: str = Field(..., min_length=1, max_length=200, description="Título da notificação")
    mensagem: str = Field(..., min_length=1, max_length=1000, description="Corpo da notificação")
    dados_extras: Optional[Dict[str, Any]] = Field(default=None, description="Dados adicionais de contexto")


class Notificacao(BaseModel):
    id: int
    destinatario_id: int
    tipo: TipoNotificacao
    titulo: str
    mensagem: str
    dados_extras: Optional[Dict[str, Any]] = None
    lida: bool = False
    criada_em: datetime

    model_config = {"from_attributes": True}
