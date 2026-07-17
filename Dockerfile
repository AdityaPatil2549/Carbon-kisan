FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY api/ ./api/

ENV PYTHONPATH=/app/backend

EXPOSE 8000

CMD ["fastapi", "run", "backend/app/main.py", "--port", "8000"]
