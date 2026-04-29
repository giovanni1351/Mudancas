"""Testes unitários do Serviço de Candidatura.

Valida a lógica interna da classe CandidaturaService e do módulo
orquestrador em isolamento, sem dependências externas ou rede.
"""

from datetime import datetime

import pytest

from servico_candidatura.models import CandidaturaCreate, CandidaturaResponse, StatusCandidatura
from servico_candidatura.orquestrador import _montar_payload
from servico_candidatura.services import CandidaturaService


@pytest.fixture
def service() -> CandidaturaService:
    """Instância limpa do serviço para cada teste."""
    return CandidaturaService()


@pytest.fixture
def payload_candidatura() -> CandidaturaCreate:
    return CandidaturaCreate(
        demanda_id=10,
        caminhoneiro_id=5,
        criador_demanda_id=3,
        mensagem="Tenho disponibilidade imediata.",
    )


class TestCriarCandidatura:
    def test_status_inicial_pendente(self, service, payload_candidatura):
        c = service.criar(payload_candidatura)
        assert c.status == StatusCandidatura.PENDENTE

    def test_id_auto_incrementado(self, service, payload_candidatura):
        c1 = service.criar(payload_candidatura)
        c2 = service.criar(payload_candidatura)
        assert c1.id == 1
        assert c2.id == 2

    def test_dados_persistidos_corretamente(self, service, payload_candidatura):
        c = service.criar(payload_candidatura)
        assert c.demanda_id == 10
        assert c.caminhoneiro_id == 5
        assert c.criador_demanda_id == 3
        assert c.mensagem == "Tenho disponibilidade imediata."
        assert isinstance(c.criada_em, datetime)
        assert isinstance(c.atualizada_em, datetime)

    def test_mensagem_pode_ser_nula(self, service):
        c = service.criar(
            CandidaturaCreate(demanda_id=1, caminhoneiro_id=2, criador_demanda_id=3)
        )
        assert c.mensagem is None


class TestListarCandidaturas:
    def test_lista_vazia_inicialmente(self, service):
        assert service.listar() == []

    def test_retorna_todas_candidaturas(self, service, payload_candidatura):
        service.criar(payload_candidatura)
        service.criar(payload_candidatura)
        assert len(service.listar()) == 2


class TestBuscarPorId:
    def test_busca_candidatura_existente(self, service, payload_candidatura):
        criada = service.criar(payload_candidatura)
        encontrada = service.buscar_por_id(criada.id)
        assert encontrada is not None
        assert encontrada.id == criada.id

    def test_retorna_none_para_id_inexistente(self, service):
        assert service.buscar_por_id(999) is None


class TestAceitarCandidatura:
    def test_muda_status_para_aceita(self, service, payload_candidatura):
        c = service.criar(payload_candidatura)
        aceita = service.aceitar(c.id)
        assert aceita is not None
        assert aceita.status == StatusCandidatura.ACEITA

    def test_atualiza_timestamp(self, service, payload_candidatura):
        c = service.criar(payload_candidatura)
        ts_antes = c.atualizada_em
        aceita = service.aceitar(c.id)
        assert aceita.atualizada_em >= ts_antes

    def test_retorna_none_se_nao_encontrada(self, service):
        assert service.aceitar(999) is None

    def test_levanta_erro_se_ja_aceita(self, service, payload_candidatura):
        c = service.criar(payload_candidatura)
        service.aceitar(c.id)
        with pytest.raises(ValueError, match="já processada"):
            service.aceitar(c.id)

    def test_levanta_erro_se_ja_rejeitada(self, service, payload_candidatura):
        c = service.criar(payload_candidatura)
        service.rejeitar(c.id)
        with pytest.raises(ValueError, match="já processada"):
            service.aceitar(c.id)


class TestRejeitarCandidatura:
    def test_muda_status_para_rejeitada(self, service, payload_candidatura):
        c = service.criar(payload_candidatura)
        rejeitada = service.rejeitar(c.id)
        assert rejeitada is not None
        assert rejeitada.status == StatusCandidatura.REJEITADA

    def test_atualiza_timestamp(self, service, payload_candidatura):
        c = service.criar(payload_candidatura)
        ts_antes = c.atualizada_em
        rejeitada = service.rejeitar(c.id)
        assert rejeitada.atualizada_em >= ts_antes

    def test_retorna_none_se_nao_encontrada(self, service):
        assert service.rejeitar(999) is None

    def test_levanta_erro_se_ja_rejeitada(self, service, payload_candidatura):
        c = service.criar(payload_candidatura)
        service.rejeitar(c.id)
        with pytest.raises(ValueError, match="já processada"):
            service.rejeitar(c.id)

    def test_levanta_erro_se_ja_aceita(self, service, payload_candidatura):
        c = service.criar(payload_candidatura)
        service.aceitar(c.id)
        with pytest.raises(ValueError, match="já processada"):
            service.rejeitar(c.id)


class TestMontarPayload:
    """Testa a função auxiliar do orquestrador que monta o payload de notificação."""

    def _candidatura_com_status(
        self, service: CandidaturaService, payload: CandidaturaCreate, status: StatusCandidatura
    ) -> CandidaturaResponse:
        c = service.criar(payload)
        c.status = status
        return c

    def test_payload_candidatura_aceita_tem_tipo_correto(self, service, payload_candidatura):
        c = self._candidatura_com_status(service, payload_candidatura, StatusCandidatura.ACEITA)
        payload = _montar_payload(c)
        assert payload["tipo"] == "CANDIDATURA_ACEITA"

    def test_payload_candidatura_rejeitada_tem_tipo_correto(self, service, payload_candidatura):
        c = self._candidatura_com_status(service, payload_candidatura, StatusCandidatura.REJEITADA)
        payload = _montar_payload(c)
        assert payload["tipo"] == "CANDIDATURA_REJEITADA"

    def test_destinatario_e_o_caminhoneiro(self, service, payload_candidatura):
        c = self._candidatura_com_status(service, payload_candidatura, StatusCandidatura.ACEITA)
        payload = _montar_payload(c)
        assert payload["destinatario_id"] == c.caminhoneiro_id

    def test_dados_extras_contem_ids_relevantes(self, service, payload_candidatura):
        c = self._candidatura_com_status(service, payload_candidatura, StatusCandidatura.ACEITA)
        payload = _montar_payload(c)
        assert payload["dados_extras"]["candidatura_id"] == c.id
        assert payload["dados_extras"]["demanda_id"] == c.demanda_id

    def test_mensagem_referencia_demanda(self, service, payload_candidatura):
        c = self._candidatura_com_status(service, payload_candidatura, StatusCandidatura.ACEITA)
        payload = _montar_payload(c)
        assert str(c.demanda_id) in payload["mensagem"]
