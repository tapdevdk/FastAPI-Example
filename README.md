# FastAPI Example

This is an example repo for creating a FastAPI application, using their "Bigger Application" structure.

The repo have been created in relation to an interview with a company called "Magenta".

## Install for development

The project have been developed using Python version `3.10.4`:

```
cd path/to/repo
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements-dev.txt
```

## Running the application in development

```
uvicorn app.main:app --reload
```

## Test requests (cURL)

Here are a couple of test `cURL`'s for using the API

**Normal routes**

```
curl --location --request GET 'localhost:8000/?token=magenta'
```

**Protected routes**

```
curl --location --request POST 'localhost:8000/admin?token=magenta' \
--header 'x-token: fake-super-secret-magenta-token'
```