# ---------- build stage ----------
FROM python:3.12-slim AS builder

WORKDIR /build

COPY pyproject.toml ./

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

# ---------- runtime stage ----------
FROM python:3.12-slim AS runtime

WORKDIR /app

# Create non-root user
RUN addgroup --system app && adduser --system --ingroup app app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY ./app ./app
COPY ./alembic ./alembic
COPY alembic.ini .

# Switch to non-root user
USER app

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
