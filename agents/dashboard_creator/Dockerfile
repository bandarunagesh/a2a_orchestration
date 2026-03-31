FROM python:3.9-slim

WORKDIR /app

COPY shared ./shared
COPY agents/dashboard_creator/requirements.txt .
RUN pip install -r requirements.txt

COPY agents/dashboard_creator .

CMD ["python", "main.py"]