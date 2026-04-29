FROM python:3.12-slim

WORKDIR /app

# Instala dependências primeiro (cache de camada)
COPY servico_candidatura/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia o pacote do serviço
COPY servico_candidatura/ ./servico_candidatura/

EXPOSE 8000

CMD ["uvicorn", "servico_candidatura.main:app", "--host", "0.0.0.0", "--port", "8000"]
