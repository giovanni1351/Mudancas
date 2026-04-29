"""Testes de integração — valida a comunicação entre os dois serviços.

Estratégia:
  - Ambos os serviços são iniciados in-process usando FastAPI TestClient (ASGI).
  - O Serviço de Candidatura normalmente usa httpx para chamar o Serviço de
    Notificação via HTTP real. Nos testes, a função `notificar_status_candidatura`
    é substituída por uma versão que usa `httpx.ASGITransport`, apontando
    diretamente para o app do Serviço de Notificação sem abrir socket de rede.
  - Isso garante testes rápidos, determinísticos e sem dependência de rede,
    mas ainda valida a integração real entre as camadas de rota e serviço
    de ambos os sistemas.
"""

import pytest
import httpx
from fastapi.testclient import TestClient

import servico_candidatura.routes as candidatura_routes
from servico_candidatura.main import app as candidatura_app
from servico_candidatura.orquestrador import _montar_payload
from servico_candidatura.services import CandidaturaService

from servico_notificacao.main import app as notificacao_app
from servico_notificacao.routes import get_service as get_notificacao_service
from servico_notificacao.services import NotificacaoService


@pytest.fixture
def servicos():
    """
    Fixture principal: sobe ambos os serviços com estado limpo e
    conecta o Serviço de Candidatura ao Serviço de Notificação via ASGITransport.
    """
    # Instâncias com estado isolado por teste
    notif_service = NotificacaoService()
    cand_service = CandidaturaService()

    # Override de dependências do FastAPI
    notificacao_app.dependency_overrides[get_notificacao_service] = lambda: notif_service
    candidatura_app.dependency_overrides[candidatura_routes.get_service] = lambda: cand_service

    # Substitui a função de notificação para usar ASGITransport (sem rede real)
    original_notificar = candidatura_routes.notificar_status_candidatura

    async def notificar_via_asgi(candidatura):
        payload = _montar_payload(candidatura)
        transport = httpx.ASGITransport(app=notificacao_app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/notificacoes/", json=payload)
            response.raise_for_status()
            return response.json()

    candidatura_routes.notificar_status_candidatura = notificar_via_asgi

    cand_client = TestClient(candidatura_app)
    notif_client = TestClient(notificacao_app)

    yield cand_client, notif_client, notif_service

    # Teardown: restaura estado original
    candidatura_routes.notificar_status_candidatura = original_notificar
    candidatura_app.dependency_overrides.clear()
    notificacao_app.dependency_overrides.clear()


class TestHealthChecks:
    def test_health_servico_candidatura(self, servicos):
        cand_client, _, _ = servicos
        resp = cand_client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["service"] == "servico_candidatura"

    def test_health_servico_notificacao(self, servicos):
        _, notif_client, _ = servicos
        resp = notif_client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["service"] == "servico_notificacao"


class TestFluxoCriacaoCandidatura:
    def test_criar_candidatura_retorna_201_e_status_pendente(self, servicos):
        cand_client, _, _ = servicos
        resp = cand_client.post(
            "/candidaturas/",
            json={
                "demanda_id": 1,
                "caminhoneiro_id": 10,
                "criador_demanda_id": 20,
                "mensagem": "Disponível para o frete.",
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["status"] == "PENDENTE"
        assert data["demanda_id"] == 1
        assert data["caminhoneiro_id"] == 10

    def test_listar_candidaturas_retorna_criadas(self, servicos):
        cand_client, _, _ = servicos
        cand_client.post(
            "/candidaturas/",
            json={"demanda_id": 1, "caminhoneiro_id": 10, "criador_demanda_id": 20},
        )
        cand_client.post(
            "/candidaturas/",
            json={"demanda_id": 2, "caminhoneiro_id": 11, "criador_demanda_id": 20},
        )
        resp = cand_client.get("/candidaturas/")
        assert resp.status_code == 200
        assert len(resp.json()) == 2

    def test_buscar_candidatura_por_id(self, servicos):
        cand_client, _, _ = servicos
        criada = cand_client.post(
            "/candidaturas/",
            json={"demanda_id": 3, "caminhoneiro_id": 12, "criador_demanda_id": 20},
        ).json()
        resp = cand_client.get(f"/candidaturas/{criada['id']}")
        assert resp.status_code == 200
        assert resp.json()["id"] == criada["id"]

    def test_buscar_candidatura_inexistente_retorna_404(self, servicos):
        cand_client, _, _ = servicos
        resp = cand_client.get("/candidaturas/999")
        assert resp.status_code == 404


class TestFluxoOrquestracao:
    """Testa o núcleo do Lab 8: a orquestração entre os dois serviços."""

    def test_aceitar_candidatura_muda_status_e_dispara_notificacao(self, servicos):
        cand_client, notif_client, notif_service = servicos

        # 1. Cria candidatura
        criada = cand_client.post(
            "/candidaturas/",
            json={"demanda_id": 10, "caminhoneiro_id": 50, "criador_demanda_id": 99},
        ).json()
        candidatura_id = criada["id"]

        # 2. Aceita — deve orquestrar notificação
        resp = cand_client.patch(f"/candidaturas/{candidatura_id}/aceitar")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ACEITA"

        # 3. Verifica que notificação foi criada no Serviço de Notificação
        notificacoes = notif_service.listar_por_destinatario(50)
        assert len(notificacoes) == 1
        assert notificacoes[0].tipo.value == "CANDIDATURA_ACEITA"
        assert notificacoes[0].dados_extras["candidatura_id"] == candidatura_id
        assert notificacoes[0].dados_extras["demanda_id"] == 10

    def test_rejeitar_candidatura_muda_status_e_dispara_notificacao(self, servicos):
        cand_client, notif_client, notif_service = servicos

        criada = cand_client.post(
            "/candidaturas/",
            json={"demanda_id": 11, "caminhoneiro_id": 51, "criador_demanda_id": 99},
        ).json()
        candidatura_id = criada["id"]

        resp = cand_client.patch(f"/candidaturas/{candidatura_id}/rejeitar")
        assert resp.status_code == 200
        assert resp.json()["status"] == "REJEITADA"

        notificacoes = notif_service.listar_por_destinatario(51)
        assert len(notificacoes) == 1
        assert notificacoes[0].tipo.value == "CANDIDATURA_REJEITADA"
        assert notificacoes[0].dados_extras["candidatura_id"] == candidatura_id

    def test_notificacao_acessivel_via_api_notificacao(self, servicos):
        """Verifica que a notificação criada pela orquestração é consultável via API."""
        cand_client, notif_client, _ = servicos

        criada = cand_client.post(
            "/candidaturas/",
            json={"demanda_id": 12, "caminhoneiro_id": 52, "criador_demanda_id": 99},
        ).json()
        cand_client.patch(f"/candidaturas/{criada['id']}/aceitar")

        resp = notif_client.get("/notificacoes/destinatario/52")
        assert resp.status_code == 200
        notificacoes = resp.json()
        assert len(notificacoes) == 1
        assert notificacoes[0]["tipo"] == "CANDIDATURA_ACEITA"

    def test_multiplas_candidaturas_geram_notificacoes_independentes(self, servicos):
        cand_client, _, notif_service = servicos

        c1 = cand_client.post(
            "/candidaturas/",
            json={"demanda_id": 20, "caminhoneiro_id": 60, "criador_demanda_id": 99},
        ).json()
        c2 = cand_client.post(
            "/candidaturas/",
            json={"demanda_id": 20, "caminhoneiro_id": 61, "criador_demanda_id": 99},
        ).json()

        cand_client.patch(f"/candidaturas/{c1['id']}/aceitar")
        cand_client.patch(f"/candidaturas/{c2['id']}/rejeitar")

        assert len(notif_service.listar_por_destinatario(60)) == 1
        assert notif_service.listar_por_destinatario(60)[0].tipo.value == "CANDIDATURA_ACEITA"

        assert len(notif_service.listar_por_destinatario(61)) == 1
        assert notif_service.listar_por_destinatario(61)[0].tipo.value == "CANDIDATURA_REJEITADA"


class TestValidacoesDeEstado:
    def test_aceitar_candidatura_inexistente_retorna_404(self, servicos):
        cand_client, _, _ = servicos
        resp = cand_client.patch("/candidaturas/999/aceitar")
        assert resp.status_code == 404

    def test_rejeitar_candidatura_inexistente_retorna_404(self, servicos):
        cand_client, _, _ = servicos
        resp = cand_client.patch("/candidaturas/999/rejeitar")
        assert resp.status_code == 404

    def test_aceitar_candidatura_ja_processada_retorna_409(self, servicos):
        cand_client, _, _ = servicos
        criada = cand_client.post(
            "/candidaturas/",
            json={"demanda_id": 30, "caminhoneiro_id": 70, "criador_demanda_id": 99},
        ).json()
        cand_client.patch(f"/candidaturas/{criada['id']}/aceitar")

        resp = cand_client.patch(f"/candidaturas/{criada['id']}/aceitar")
        assert resp.status_code == 409

    def test_rejeitar_candidatura_ja_processada_retorna_409(self, servicos):
        cand_client, _, _ = servicos
        criada = cand_client.post(
            "/candidaturas/",
            json={"demanda_id": 31, "caminhoneiro_id": 71, "criador_demanda_id": 99},
        ).json()
        cand_client.patch(f"/candidaturas/{criada['id']}/rejeitar")

        resp = cand_client.patch(f"/candidaturas/{criada['id']}/rejeitar")
        assert resp.status_code == 409
