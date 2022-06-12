# FastAPI Example

This is an example repo for creating a FastAPI application, using their "Bigger Application" structure as a template and then
made into a more interesting application with postgres, docker etc.

Contents:

* Install for development 
* Running the application in development
* Database schema install (runtime)
* Development requests
* Docker build & run
* Testing

## Install for development

The project have been developed using Python version `3.10.4`:

```shell
cd path/to/repo
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements-dev.txt
```

## Running the application in development

```shell
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
            "justMyCode": true,
            "args": [
                "app.main:app"
            ]
        }
    ]
}
```

## Database schema install (runtime)

When the application is up, the database schema can be installed using the following cURL command:

```shell
curl --location --request GET 'localhost:8000/admin/db/install?token=magenta' \
--header 'x-token: fake-super-secret-magenta-token'
```
INFO: The file `<path-to-repo>/schema.sql` will be executed on the connected database.

**IMPORTANT!**

The `/admin/db/install`-route was implemented as a quick and dirty way to implement the database schema. We would not recommend doing this in any production environments, and should ultimatly be removed from sunch environments.

## Development requests (cURL)

Here are a couple of test `cURL`'s requests for using the API in development

```shell
# Root route
curl --location --request GET 'localhost:8000/?token=magenta'

# Get blogs
curl --location --request GET 'localhost:8000/blogs/?token=magenta' \
--header 'x-token: fake-super-secret-magenta-token'

# Get accounts
curl --location --request GET 'localhost:8000/accounts/?token=magenta' \
--header 'x-token: fake-super-secret-magenta-token'

# Authenticate account
curl --location --request POST 'localhost:8000/accounts/authenticate?token=magenta' \
--header 'x-token: fake-super-secret-magenta-token' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "test",
    "password": "mypassword"
}'
```

## Docker build & run

```shell
cd path/to/repo
docker build -t thorastrup-fastapi-example .
docker run -d --name fastapitest -p 8001:80 thorastrup-fastapi-example
```
OBS: Change port `8001` to your liking

**NOTE:**

We do not configure anything about the network in above commands.
So if you are running this docker container on your local development computer and you want it to connect to your development PostgreSQL database,
you will ned to specify the `DB_HOSTNAME`-environment variable, ex `192.168.0.137`:

```shell
docker run -e DB_HOSTNAME=<your-local-ip> -d --name fastapitest -p 8001:80 thorastrup-fastapi-example
```

or of course configure the network part differently :-)

## Testing

Execute the following commands to run the tests:

```shell
cd path/to/repo
source venv/bin/activate
python -m pytest tests
```

OBS: Its import to use the `python -m`-prefix, in order for pytest to import the app-module.

**VSCode launch.json config:**

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Testing",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "justMyCode": true,
            "args": [
                "tests"
            ],
        },
    ]
}
```

## CI/CD

The applications CI/CD, is maintained by the CircleCI and the config can be found in `.circleci/config.yml`.

**Workflows:**

* build-publish-latest
    * Triggers on all updates to `main`-branch
    * Builds the latest `main`-branch and pushes it to docker-hub with tag: `latest`
* build-publish-tag
    * Triggers on created tags with the format: `{integer}.{integer}.{integer}`
    * Builds the newly created tag and pushes it to docker-hub with the tag: `<newly-created-git-tag>` AND `latest`
        * Not sure about pushing it to the `latest`-tag, but the idea was that this tag should also contain the latest build. But i would say it could be argumented that it should just be the latest build of the `main`-branch.