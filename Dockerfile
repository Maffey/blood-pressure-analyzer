# syntax=docker/dockerfile:1

# Builder
FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim AS builder

# Faster, more reproducible installs inside containers.
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Install dependencies first (without the project) so this layer is cached
# and only re-runs when the lockfile or pyproject change.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Install the project itself.
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Runtime
FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim AS runtime

WORKDIR /app

# Run as an unprivileged user.
RUN useradd --create-home --uid 1000 app

# Copy the resolved virtualenv and application code from the builder.
COPY --from=builder --chown=app:app /app /app

# Put the venv on PATH so `streamlit` is resolvable directly.
ENV PATH="/app/.venv/bin:$PATH"

USER app

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8501/_stcore/health').status==200 else 1)"

# `static/images/droplet_solid.svg` is referenced relatively, so launch from /app.
ENTRYPOINT ["streamlit", "run", "src/blood_pressure_analyzer/__main__.py", \
    "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
