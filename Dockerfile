FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN useradd -m user && \
    mkdir -p /app && \
    chown -R user:user /app

COPY --chown=user:user . .

USER user

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && python src/main.py"]
