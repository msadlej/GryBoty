FROM python:3.11-slim
WORKDIR /code
COPY / /code
COPY requirements.txt /app/ 
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH=/code