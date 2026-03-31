FROM python:3.9-slim

WORKDIR /app

COPY shared ./shared
COPY agents/notifications/requirements.txt .
RUN pip install -r requirements.txt

COPY agents/notifications .

CMD ["python", "main.py"]