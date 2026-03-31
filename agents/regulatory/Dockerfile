FROM python:3.9-slim

WORKDIR /app

COPY shared ./shared
COPY agents/regulatory/requirements.txt .
RUN pip install -r requirements.txt

COPY agents/regulatory .

CMD ["python", "main.py"]