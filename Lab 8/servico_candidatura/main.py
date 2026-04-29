from fastapi import FastAPI

from .routes import router

app = FastAPI(
    title="Serviço de Candidatura — Mudapp",
    description=(
        "Gerencia candidaturas de caminhoneiros a demandas de frete. "
        "Atua como **orquestrador**: ao aceitar ou rejeitar uma candidatura, "
        "coordena ativamente o envio de notificações via Serviço de Notificação."
    ),
    version="1.0.0",
    contact={"name": "Equipe Mudapp"},
)

app.include_router(router)


@app.get("/health", tags=["Saúde"], summary="Health check")
def health_check() -> dict:
    return {"status": "ok", "service": "servico_candidatura"}
