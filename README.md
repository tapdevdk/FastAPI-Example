# FastAPI Example

This is an example repo for creating a FastAPI application, using their "Bigger Application" structure.

The repo have been created in relation to an interview with a company called "Magenta".

Contents:

* Install for development 
* Running the application in development
* Development requests
* Docker build & run

## Development install

The project have been developed using Python version `3.10.4`:

```
cd path/to/repo
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements-dev.txt
```

## Running the application in development

```
docker-compose up -d
uvicorn app.main:app --reload
```

**VSCode launch.json for debugging:**

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "app.main:app"
            ],
            "jinja": true,
            "justMyCode": true
        }
    ]
}
```

## Development requests (cURL)

Here are a couple of test `cURL`'s for using the API

**Root route:**

```
curl --location --request GET 'localhost:8000/?token=magenta'
```
c
**Admin POST page handler:**

```
curl --location --request POST 'localhost:8000/admin?token=magenta' \
--header 'x-token: fake-super-secret-magenta-token'
```

**Get blogs:**

```
curl --location --request GET 'localhost:8000/blogs?token=magenta' \
--header 'x-token: fake-super-secret-magenta-token'
```

## Docker build & run

**Building the docker image:**

```
cd path/to/repo
docker build -t thorastrup-fastapi-example .
```

**Run the docker image:**

```
docker run -d --name fastapitest -p 8001:80 thorastrup-fastapi-example
```
OBS: Change port `8001` to your liking