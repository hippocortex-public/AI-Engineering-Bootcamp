FROM python:3.12-slim
WORKDIR /app
RUN useradd --uid 10001 --create-home appuser && mkdir /data && chown appuser:appuser /data
COPY . /app/examples/week07/
USER appuser
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 WORKFLOW_HOST=0.0.0.0 WORKFLOW_DB=/data/workflow.sqlite
EXPOSE 8080
CMD ["python", "-m", "examples.week07.server"]
