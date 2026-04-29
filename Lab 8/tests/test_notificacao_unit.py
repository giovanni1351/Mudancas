"""Testes unitários do Serviço de Notificação.

Valida a lógica interna da classe NotificacaoService em isolamento,
sem dependências externas ou rede.
"""

from datetime import datetime

import pytest

from servico_notificacao.models import NotificacaoCreate, TipoNotificacao
from servico_notificacao.services import NotificacaoService


@pytest.fixture
def service() -> NotificacaoService:
    """Instância limpa do serviço para cada teste."""
    return NotificacaoService()


@pytest.fixture
def payload_info() -> NotificacaoCreate:
    return NotificacaoCreate(
        destinatario_id=1,
        tipo=TipoNotificacao.INFO,
        titulo="Informação",
        mensagem="Mensagem de teste",
    )


class TestCriarNotificacao:
    def test_id_auto_incrementado(self, service, payload_info):
        n1 = service.criar(payload_info)
        n2 = service.criar(payload_info)
        assert n1.id == 1
        assert n2.id == 2

    def test_dados_persistidos_corretamente(self, service):
        data = NotificacaoCreate(
            destinatario_id=42,
            tipo=TipoNotificacao.CANDIDATURA_REJEITADA,
            titulo="Candidatura rejeitada",
            mensagem="Não foi selecionado.",
            dados_extras={"demanda_id": 7},
        )
        n = service.criar(data)

        assert n.destinatario_id == 42
        assert n.tipo == TipoNotificacao.CANDIDATURA_REJEITADA
        assert n.titulo == "Candidatura rejeitada"
        assert n.mensagem == "Não foi selecionado."
        assert n.dados_extras == {"demanda_id": 7}
        assert n.lida is False
        assert isinstance(n.criada_em, datetime)

    def test_notificacao_inicia_como_nao_lida(self, service, payload_info):
        n = service.criar(payload_info)
        assert n.lida is False

    def test_dados_extras_podem_ser_nulos(self, service, payload_info):
        n = service.criar(payload_info)
        assert n.dados_extras is None


class TestListarNotificacoes:
    def test_lista_vazia_inicialmente(self, service):
        assert service.listar() == []

    def test_retorna_todas_notificacoes_criadas(self, service, payload_info):
        service.criar(payload_info)
        service.criar(payload_info)
        assert len(service.listar()) == 2

    def test_retorna_lista_imutavel_do_estado_interno(self, service, payload_info):
        service.criar(payload_info)
        lista = service.listar()
        lista.clear()
        assert len(service.listar()) == 1  # estado interno não deve ser afetado


class TestBuscarPorId:
    def test_busca_notificacao_existente(self, service, payload_info):
        criada = service.criar(payload_info)
        encontrada = service.buscar_por_id(criada.id)
        assert encontrada is not None
        assert encontrada.id == criada.id

    def test_retorna_none_para_id_inexistente(self, service):
        assert service.buscar_por_id(999) is None

    def test_retorna_none_quando_bd_vazio(self, service):
        assert service.buscar_por_id(1) is None


class TestListarPorDestinatario:
    def test_filtra_corretamente_por_destinatario(self, service):
        for dest_id in [1, 1, 2, 3]:
            service.criar(
                NotificacaoCreate(
                    destinatario_id=dest_id,
                    tipo=TipoNotificacao.INFO,
                    titulo="t",
                    mensagem="m",
                )
            )
        resultado = service.listar_por_destinatario(1)
        assert len(resultado) == 2
        assert all(n.destinatario_id == 1 for n in resultado)

    def test_retorna_lista_vazia_para_destinatario_sem_notificacoes(self, service):
        assert service.listar_por_destinatario(99) == []
