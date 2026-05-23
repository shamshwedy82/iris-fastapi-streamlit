# Troubleshooting

## Error: No module named uvicorn

Make sure requirements.txt contains:

```text
uvicorn[standard]
gunicorn
```

Also add this Azure Application Setting:

```text
SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

## Error: No module named sklearn

Make sure requirements.txt contains:

```text
scikit-learn
```

## Error: model file not found

Make sure this file exists and is deployed:

```text
models/iris_model.joblib
```

## Error: Cannot import module main

Check the startup command.

If your file is:

```text
main.py
```

and inside it:

```python
app = FastAPI()
```

then startup command should be:

```bash
gunicorn -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 main:app
```

## Error: Application Error after deploy

Go to:

```text
Azure Portal > App Service > Log stream
```

Most problems are from:

```text
wrong startup command
missing package in requirements.txt
missing model file
wrong Python version
```
