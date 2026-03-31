FROM python:3.9-slim

WORKDIR /app

COPY shared ./shared
COPY agents/forecasting/requirements.txt .
RUN pip install -r requirements.txt

COPY agents/forecasting .

CMD ["python", "main.py"]