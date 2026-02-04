FROM python:3.13-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc ca-certificates \
 && rm -rf /var/lib/apt/lists/*

RUN groupadd -r appgroup && useradd -r -g appgroup -d /home/appuser -m -s /sbin/nologin appuser

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 5000

ENV HOST=0.0.0.0
ENV PORT=5000

# Default command
CMD ["python", "app.py"]
