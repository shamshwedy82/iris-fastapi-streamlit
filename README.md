# Azure FastAPI Machine Learning Full Project

This is a complete project for deploying a Machine Learning model served by FastAPI to Azure App Service.

## Project Structure

```text
azure_fastapi_ml_full_project/
├── main.py
├── train_model.py
├── requirements.txt
├── startup.txt
├── models/
│   └── iris_model.joblib
├── sample_requests/
│   ├── predict_single.json
│   ├── predict_batch.json
│   ├── api_requests.http
│   └── test_api.py
├── deployment_notes/
│   ├── azure_portal_steps.md
│   ├── azure_cli_zip_deploy.md
│   └── troubleshooting.md
└── README.md
```

## What this project does

The project trains a simple Iris flower classification model using scikit-learn and serves it through FastAPI.

Available endpoints:

```text
GET  /
GET  /health
GET  /model-info
POST /predict
POST /predict-batch
```

## 1. Create environment locally

Using Conda:

```bash
conda create -n fastapi_azure_ml python=3.12 -y
conda activate fastapi_azure_ml
```

## 2. Install requirements

```bash
pip install -r requirements.txt
```

## 3. Train the model

```bash
python train_model.py
```

This creates:

```text
models/iris_model.joblib
```

The ZIP already includes a trained model, but you can regenerate it anytime.

## 4. Run locally

```bash
python -m uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## 5. Azure App Service Startup Command

Use this in Azure App Service > Configuration > General settings > Startup Command:

```bash
gunicorn -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 main:app
```

## 6. Azure App Service Application Setting

Add this setting:

```text
SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

## 7. Test after deployment

Open:

```text
https://YOUR_APP_NAME.azurewebsites.net/docs
```

Then test:

```text
POST /predict
```

Example JSON:

```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

## Teaching explanation

FastAPI does not train the model.

FastAPI serves the trained model through API endpoints.

The flow is:

```text
User sends JSON
      ↓
FastAPI validates input
      ↓
FastAPI converts input to NumPy array
      ↓
ML model predicts
      ↓
FastAPI returns JSON response
```
