# Multi-Service-API-with-FastAPI-Go-Machine-Learning
A high-performance multi-service backend combining FastAPI, Go, and Python ML models. Built with a modern microservice architecture supporting ultra-fast inference, scalable design, and production-ready APIs.

Nice — thanks for the screenshot. I updated the README to match your actual repo layout (no Go). Below is a **copy–paste ready `README.md`** tailored to the structure you provided.

---

# ⚡ Multi-Service API (FastAPI + Python ML)

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-brightgreen)
![Machine Learning](https://img.shields.io/badge/ML-Enabled-orange)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)


## Table of contents

* [Repository structure](#repository-structure)
* [Features](#features)
* [Models & files included](#models--files-included)
* [Installation & running](#installation--running)
* [Docker](#docker)
* [API endpoints (example)](#api-endpoints-example)
* [Development & testing](#development--testing)
* [Commit message guidelines](#commit-message-guidelines)
* [Contributing](#contributing)
* [License](#license)

---

## Repository structure

```
api service/
├── app/
│   ├── modules/
│   │   ├── series_analyzer/
│   │   │   └── service.py
│   │   └── stock_predictor/
│   │       ├── __pycache__/
│   │       ├── model/
│   │       │   ├── max.npy
│   │       │   ├── min.npy
│   │       │   └── stock_ann.h5
│   │       ├── model_loader.py
│   │       └── routes.py
│   ├── templates/
│   │   └── api_guide.html
│   └── __init__.py
├── .dockerignore
├── Dockerfile
├── main.py
├── multiserivce-api.tar
├── requirements.txt
├── test.py
├── test.csv
└── train.csv


## Features

* FastAPI gateway (`main.py`) — single entrypoint to all micro-services.
* Modular service layout — each ML feature is isolated under `app/modules/<service_name>`.
* Stock prediction service uses a pre-trained Keras model (`stock_ann.h5`) and normalization arrays (`min.npy`, `max.npy`).
* Time-series analyzer under `series_analyzer/` for trend/seasonality functions.
* Lightweight HTML API guide served from `templates/api_guide.html`.
* Docker-ready for reproducible deployments.

---

## Models & files included

* `app/modules/stock_predictor/model/stock_ann.h5` — trained Keras model for stock prediction.
* `app/modules/stock_predictor/model/min.npy` and `max.npy` — arrays used to scale/normalize inputs.
* Example CSVs: `train.csv`, `test.csv` — sample datasets used for training/testing.
* `app/modules/stock_predictor/model_loader.py` — helper to load model + scalers safely.
* `app/modules/stock_predictor/routes.py` — REST endpoints for prediction.

---

## Installation & running (local, non-Docker)

1. Clone repository

```bash
git clone https://github.com/your-username/your-repo.git
cd "api service"
```

2. Create virtual environment & install dependencies

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt
```

3. Run the app (development)

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

4. Visit:

* API root: `http://localhost:8000/`
* OpenAPI docs: `http://localhost:8000/docs`
* API guide (HTML): `http://localhost:8000/api-guide` *(routes may vary — see `main.py`/`routes.py`)*

---

## Docker

Build & run using the provided `Dockerfile`:

```bash
# build
docker build -t multi-service-api:latest .

# run
docker run -p 8000:8000 --rm multi-service-api:latest
```

If you prefer docker-compose (create a simple `docker-compose.yml` mapping ports and volumes), you can spin up the containerized service for production testing.

---

## Example API endpoints (adapt to your `routes.py`)

> These are suggested endpoints based on your folder names. Adjust to the actual paths in your `routes.py`.

* `POST /stock/predict`
  Body (JSON):

  ```json
  {
    "features": [ /* numeric input vector matching model input shape */ ]
  }
  ```

  Response:

  ```json
  { "prediction": 123.45, "scaled": false }
  ```

* `POST /series/analyze`
  Body (JSON):

  ```json
  {
    "series": [1,2,3,4,5],
    "freq": "D"
  }
  ```

  Response:

  ```json
  { "trend": [...], "seasonality": [...], "summary": {...} }
  ```

* `GET /api-guide`
  Returns the `api_guide.html` template (simple documentation page).

* `GET /docs`
  FastAPI-generated Swagger UI.

> Put endpoint examples and sample requests/responses in the README or in `api_guide.html` for easy onboarding.

---

## Development & testing

* Run `test.py` to exercise unit/smoke tests (adapt `test.py` to call your routes).
* Update model artifacts under `app/modules/stock_predictor/model/` (if retraining).
* Use `model_loader.py` to centralize model-loading logic — this prevents reloading the model on each request.

---

## Security & Production Notes

* Don't commit training data or large model files to the repo in production; use an artifact store or cloud storage.
* If you expose model endpoints publicly:

  * Add authentication (JWT) and rate limiting.
  * Validate & sanitize all inputs to avoid unexpected shapes or types.
  * Use Gunicorn + Uvicorn workers for production.
  * Use volume mounts for model files to update models without rebuilding images.

---

## Commit message guidelines

Use conventional commits to keep history readable:

```
feat(stock): add prediction endpoint
fix(stock): correct input scaling bug
docs: update API examples
test: add unit test for model_loader
chore: bump requirements
```

---

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feat/my-feature`.
3. Commit changes and open a PR with a description of changes + motivation.
4. Run tests and ensure code is linted before merging.

---

## License

This project is licensed under the **MIT License** — see `LICENSE` file.


T
