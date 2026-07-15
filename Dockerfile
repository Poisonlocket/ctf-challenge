FROM python:3.11.15-slim-bookworm AS builder

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.11.15-slim-bookworm

RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

WORKDIR /app

RUN touch ./flag.txt && chown appuser:appgroup ./flag.txt
COPY --from=builder --chown=appuser:appgroup /opt/venv /opt/venv
COPY --chown=appuser:appgroup main.py .

USER appuser
ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 