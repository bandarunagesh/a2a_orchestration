FROM python:3.9-slim

WORKDIR /app

COPY shared ./shared
COPY orchestrator_gateway/requirements.txt .
RUN pip install -r requirements.txt

COPY orchestrator_gateway .

CMD ["python", "main.py"]