FROM python:3.9-slim

WORKDIR /app

COPY shared ./shared
COPY agents/conduct/requirements.txt .
RUN pip install -r requirements.txt

COPY agents/conduct .

CMD ["python", "main.py"]