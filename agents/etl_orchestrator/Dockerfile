FROM python:3.9-slim

WORKDIR /app

COPY shared ./shared
COPY agents/etl_orchestrator/requirements.txt .
RUN pip install -r requirements.txt

COPY agents/etl_orchestrator .

CMD ["python", "main.py"]