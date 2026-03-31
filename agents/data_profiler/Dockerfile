FROM python:3.9-slim

WORKDIR /app

COPY shared ./shared
COPY agents/data_profiler/requirements.txt .
RUN pip install -r requirements.txt

COPY agents/data_profiler .

CMD ["python", "main.py"]