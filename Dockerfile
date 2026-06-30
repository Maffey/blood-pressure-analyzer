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

# Streamlit reads these natively, so the listen port can be overridden by the
# host (Fly sets none and uses 8501; Railway/Render/Cloud Run inject $PORT and
# you point STREAMLIT_SERVER_PORT at it) without rebuilding the image.
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_HEADLESS=true

USER app

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import os,urllib.request,sys; p=os.environ.get('STREAMLIT_SERVER_PORT','8501'); sys.exit(0 if urllib.request.urlopen(f'http://localhost:{p}/_stcore/health').status==200 else 1)"

# `static/images/droplet_solid.svg` is referenced relatively, so launch from /app.
ENTRYPOINT ["streamlit", "run", "src/blood_pressure_analyzer/__main__.py"]
