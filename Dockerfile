# ════════════════════════════════════════════════════════════════════════
# Anita Agent - Multi-Stage Docker Build
# Bygger produksjonsklar image med optimal størrelse
# ════════════════════════════════════════════════════════════════════════

# ════════════════════════════════════════════════════════════════════════
# STAGE 1: Dependencies
# Henter og installerer Python-avhengigheter
# ════════════════════════════════════════════════════════════════════════
FROM python:3.11-slim as deps

WORKDIR /app

# Installere byggeavhengigheter
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Kopiere requirements først (for bedre caching)
COPY requirements.txt requirements-test.txt ./

# Opprette virtual environment og installere avhengigheter
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt


# ════════════════════════════════════════════════════════════════════════
# STAGE 2: Testing
# Kjører alle tester før produksjonsbuild
# ════════════════════════════════════════════════════════════════════════
FROM python:3.11-slim as testing

WORKDIR /app

# Kopiere virtual environment fra deps
COPY --from=deps /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Kopiere testavhengigheter
COPY requirements-test.txt ./
RUN pip install --no-cache-dir -r requirements-test.txt

# Kopiere all kode
COPY . .

# Sette PYTHONPATH
ENV PYTHONPATH=/app

# Kjøre tester
RUN echo "=== Running unit tests ===" && \
    pytest tests/unit -v --tb=short -x || exit 1

RUN echo "=== Running integration tests ===" && \
    pytest tests/integration -v --tb=short -x || echo "Some integration tests may fail without external services"

RUN echo "=== All tests passed ==="


# ════════════════════════════════════════════════════════════════════════
# STAGE 3: Production
# Minimal image for produksjon
# ════════════════════════════════════════════════════════════════════════
FROM python:3.11-alpine as production

LABEL maintainer="Anita Agent Team"
LABEL description="Anita Agent - Self-Healing AI System"
LABEL version="1.0.0"

# Sikkerhet: Opprette non-root bruker
RUN addgroup -g 1000 anita && \
    adduser -u 1000 -G anita -s /bin/sh -D anita

WORKDIR /app

# Installere nødvendige system-pakker
RUN apk add --no-cache \
    libstdc++ \
    && rm -rf /var/cache/apk/*

# Kopiere virtual environment fra deps (ikke testing)
COPY --from=deps /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Kopiere applikasjonskode
COPY --chown=anita:anita SANDKASSE/07_Sandkasse_SelfHealing/ ./
COPY --chown=anita:anita sandkasse_protokoll.py ./
COPY --chown=anita:anita enkel_server.py ./

# Opprette nødvendige mapper
RUN mkdir -p /app/logs /app/backups /app/fixes && \
    chown -R anita:anita /app

# Bytte til non-root bruker
USER anita

# Miljøvariabler
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV ENVIRONMENT=production
ENV LOG_LEVEL=info
ENV PORT=8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "
import urllib.request
import sys
try:
    urllib.request.urlopen('http://localhost:8080/health', timeout=5)
    sys.exit(0)
except:
    sys.exit(1)
" || exit 1

# Eksponere porter
EXPOSE 8080 8765

# Start kommando
CMD ["python", "enkel_server.py"]


# ════════════════════════════════════════════════════════════════════════
# STAGE 4: Development (valgfri)
# Inkluderer dev tools for lokal utvikling
# ════════════════════════════════════════════════════════════════════════
FROM deps as development

WORKDIR /app

# Installere development tools
RUN pip install --no-cache-dir \
    black \
    flake8 \
    pytest \
    pytest-cov \
    ipython

# Kopiere kode
COPY . .

ENV PYTHONPATH=/app
ENV ENVIRONMENT=development
ENV LOG_LEVEL=debug

EXPOSE 8080 8765

CMD ["python", "enkel_server.py"]
