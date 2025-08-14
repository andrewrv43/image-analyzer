FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install deps first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade openai
# Copy source
COPY . .

ENV APP_ENV=prod \
    PORT=8000 \
    MAX_CONTENT_LENGTH=5242880 \
    PYTHONPATH=/app

EXPOSE 8000

# Use gunicorn in container (module:variable)
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app", "--workers", "2", "--threads", "4", "--timeout", "60"]
