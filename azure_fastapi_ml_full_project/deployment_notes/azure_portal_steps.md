# Azure Portal Deployment Steps

## 1. Create Web App

Go to Azure Portal:

```text
Create a resource > Web App
```

Use:

```text
Publish: Code
Runtime stack: Python 3.12
Operating System: Linux
Region: choose nearest region
Pricing Plan: Free or Basic for testing
```

## 2. Add Startup Command

Go to:

```text
App Service > Configuration > General settings > Startup Command
```

Add:

```bash
gunicorn -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 main:app
```

Click Save, then Restart.

## 3. Add Application Setting

Go to:

```text
App Service > Configuration > Application settings
```

Add:

```text
SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

## 4. Deploy the Code

You can deploy using:

- VS Code Azure App Service Extension
- Azure CLI ZIP Deploy
- GitHub Actions
- Deployment Center

## 5. Test

Open:

```text
https://YOUR_APP_NAME.azurewebsites.net/docs
```

Test:

```text
GET /health
POST /predict
```
