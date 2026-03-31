FROM python:3.9-slim

WORKDIR /app

COPY shared ./shared
COPY agents/insights/requirements.txt .
RUN pip install -r requirements.txt

COPY agents/insights .

CMD ["python", "main.py"]