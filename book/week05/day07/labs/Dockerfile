FROM python:3.12-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY requirements.lock .
RUN python -m pip install --no-cache-dir -r requirements.lock \
    && groupadd --gid 10001 app \
    && useradd --uid 10001 --gid 10001 --no-create-home --shell /usr/sbin/nologin app
COPY deployment_ai_service ./deployment_ai_service
USER 10001:10001
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "deployment_ai_service.app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--no-access-log", "--timeout-graceful-shutdown", "20"]
