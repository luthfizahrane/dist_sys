FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends libxml2 libxslt1.1 && rm -rf /var/lib/apt/lists/*
COPY SOAP/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY SOAP/ /app/
EXPOSE 8000
CMD ["python", "server.py"]