FROM python:3.9-slim

WORKDIR /app

COPY shared ./shared
COPY agents/analyst/requirements.txt .
RUN pip install -r requirements.txt

COPY agents/analyst .

CMD ["python", "main.py"]