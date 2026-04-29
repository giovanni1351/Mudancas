from fastapi import FastAPI

from .routes import router

app = FastAPI(
    title="Serviço de Notificação — Mudapp",
    description=(
        "Responsável por armazenar e entregar notificações aos usuários do Mudapp. "
        "Recebe chamadas HTTP do Serviço de Candidatura (orquestração)."
    ),
    version="1.0.0",
    contact={"name": "Equipe Mudapp"},
)

app.include_router(router)


@app.get("/health", tags=["Saúde"], summary="Health check")
def health_check() -> dict:
    return {"status": "ok", "service": "servico_notificacao"}
