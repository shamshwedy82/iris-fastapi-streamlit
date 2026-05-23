# Azure CLI ZIP Deploy

## 1. Login

```bash
az login
```

## 2. Create ZIP

Important: zip the content of the project folder, not the parent folder.

The ZIP should contain files directly like:

```text
main.py
requirements.txt
models/iris_model.joblib
```

## 3. Deploy

```bash
az webapp deploy ^
  --resource-group YOUR_RESOURCE_GROUP ^
  --name YOUR_APP_SERVICE_NAME ^
  --src-path azure_fastapi_ml_full_project.zip ^
  --type zip
```

For PowerShell, use backticks instead of `^`.

## 4. Restart

```bash
az webapp restart ^
  --resource-group YOUR_RESOURCE_GROUP ^
  --name YOUR_APP_SERVICE_NAME
```
