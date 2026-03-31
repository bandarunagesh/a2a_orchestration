FROM python:3.9-slim

WORKDIR /app

COPY shared ./shared
COPY agents/report_builder/requirements.txt .
RUN pip install -r requirements.txt

COPY agents/report_builder .

CMD ["python", "main.py"]