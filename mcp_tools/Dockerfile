FROM python:3.9-slim

WORKDIR /app

COPY mcp_tools/requirements.txt .
RUN pip install -r requirements.txt

COPY mcp_tools .

CMD ["python", "main.py"]