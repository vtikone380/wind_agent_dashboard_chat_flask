# Wind Turbine Flask Dashboard

A small dynamic Flask dashboard project for Azure App Service deployment.

## Local run on Windows

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Azure startup command

```bash
gunicorn --bind=0.0.0.0:8000 app:app
```

## Environment variable example

```text
APP_NAME=Vinayak Turbine Dashboard
```
