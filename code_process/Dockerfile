FROM python:3.11-slim
WORKDIR /app

# Install dependencies for Ice (use pip package zeroc-ice)
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libssl-dev libbz2-dev && rm -rf /var/lib/apt/lists/*

COPY code_process/ /app/code_process/
WORKDIR /app/code_process

# Install Python Ice runtime
RUN pip install --no-cache-dir zeroc-ice==3.7.10

# Generate Python stubs from Slice definition
RUN slice2py Demo.ice || (echo "slice2py not found in PATH - ensure zeroc-ice provides it" && exit 1)

ENV PYTHONPATH=/app/code_process

CMD ["python", "multiprcs.py"]