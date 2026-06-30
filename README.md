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
