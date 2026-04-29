FROM python:3.12-slim

WORKDIR /app

# Instala dependências primeiro (cache de camada)
COPY servico_notificacao/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia o pacote do serviço
COPY servico_notificacao/ ./servico_notificacao/

EXPOSE 8001

CMD ["uvicorn", "servico_notificacao.main:app", "--host", "0.0.0.0", "--port", "8001"]
