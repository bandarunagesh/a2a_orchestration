FROM python:3.9-slim

WORKDIR /app

COPY shared ./shared
COPY agents/closeout/requirements.txt .
RUN pip install -r requirements.txt

COPY agents/closeout .

CMD ["python", "main.py"]