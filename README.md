# blood-pressure-analyzer

Analyze your blood pressure data based on exported CSV from BP Journal app.

## To run

Windows: `uv run streamlit run .\src\blood_pressure_analyzer\__main__.py`

Linux: `uv run streamlit run src/blood_pressure_analyzer/__main__.py`

## Docker

The image is built on the [official `uv` images](https://github.com/astral-sh/uv)
(Python 3.14) using a multi-stage, layer-cached build.

Build:

```bash
docker build -t blood-pressure-analyzer .
```

Run (the app is served on port `8501`):

```bash
docker run --rm -p 8501:8501 blood-pressure-analyzer
```

Then open http://localhost:8501.

The listen port can be overridden without rebuilding via `STREAMLIT_SERVER_PORT`
(e.g. for hosts that inject a `$PORT`).

## Deploy to Fly.io

The image and [`fly.toml`](./fly.toml) are ready to deploy. With the
[`fly` CLI](https://fly.io/docs/flyctl/install/) installed and `fly auth login` done:

```bash
# First time only: claim a unique app name and region (keeps the existing fly.toml).
fly launch --no-deploy

# Deploy (builds the Dockerfile and ships it).
fly deploy

# Open the running app.
fly open
```

The app scales to zero when idle (`auto_stop_machines`), so it costs nothing
between visits and cold-starts on the next request.
