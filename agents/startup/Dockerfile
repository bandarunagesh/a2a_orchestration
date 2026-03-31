FROM python:3.9-slim

WORKDIR /app

COPY shared ./shared
COPY agents/startup/requirements.txt .
RUN pip install -r requirements.txt

COPY agents/startup .

CMD ["python", "main.py"]