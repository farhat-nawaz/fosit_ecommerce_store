# Fosit Ecommerce Store

This is a back-end API that powers a web admin dashboard for e-commerce managers. This API provides detailed insights into sales, revenue, and inventory status, as well as allows new product registration. It has been implemented using Python and FastAPI.


## Configuration

This application can be configured with environment variables.

You can create `.env` file in the root directory and place all
environment variables here.

All environment variables should start with "FOSIT_ECOMMERCE_STORE_" prefix.

For example if you see in your "fosit_ecommerce_store/settings.py" a variable named like
`random_parameter`, you should provide the "FOSIT_ECOMMERCE_STORE_RANDOM_PARAMETER"
variable to configure the value.

Following env vers must be set for MySQL connection:
```bash
FOSIT_ECOMMERCE_STORE_DB_USER=root
FOSIT_ECOMMERCE_STORE_DB_PASS=mysql
FOSIT_ECOMMERCE_STORE_DB_NAME=fosit_ecommerce_store
```
You can have different values for MySQL config.


## Docker

You can start the project with docker using this command:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . up --build
```

The app should be running on `http://127.0.0.1:8000`.

## API Documentation

API endpoints are available at `/api`. Full OpenAPI specification can be found at `/api/redoc` and `/api/docs`.

## Sample Data
A sql script is included in the project to get started with some sample data. A `cli` utility can be
used to perform operations like these from the terminal.

Once the containers are up, run the following command to load data into the database.

```bash
docker exec -it api_container python cli.py db load-sample-data
```


## Running using Poetry

This project also uses poetry. It's a modern dependency management
tool.

To run the project with poetry, use this set of commands:

```bash
poetry install
poetry run python -m fosit_ecommerce_store
```

This will start the server on the configured host.


## Project structure

```bash
$ tree "fosit_ecommerce_store"
fosit_ecommerce_store
├── conftest.py  # Fixtures for all tests.
├── db  # module contains db configurations
│   ├── dao  # Data Access Objects. Contains different classes to interact with database.
│   └── models  # Package contains different models for ORMs.
├── __main__.py  # Startup script. Starts uvicorn.
├── settings.py  # Main configuration settings for project.
├── static  # Static content.
├── tests  # Tests for project.
└── web  # Package contains web server. Handlers, startup config.
    ├── api  # Package with all handlers.
    │   └── router.py  # Main router.
    ├── application.py  # FastAPI application configuration.
    └── lifetime.py  # Contains actions to perform on startup and shutdown.
```

## Pre-commit

To install pre-commit simply run inside the shell:
```bash
pre-commit install
```

pre-commit is very useful to check your code before publishing it.
It's configured using .pre-commit-config.yaml file.

By default it runs:
* black (formats your code);
* mypy (validates types);
* isort (sorts imports in all files);
* flake8 (spots possible bugs);



## Migrations

If you want to migrate your database, you should run following commands:
```bash
# Upgrade database to the last migration.
aerich upgrade
```

### Reverting migrations

If you want to revert migrations, you should run:
```bash
aerich downgrade
```

### Migration generation

To generate migrations you should run:
```bash
aerich migrate
```


## Running tests

If you want to run it in docker, simply run:

```bash
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . run --build --rm api pytest -vv .
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . down
```

For running tests on your local machine.
1. you need to start a database.

I prefer doing it with docker:
```
docker run -p "3306:3306" -e "MYSQL_PASSWORD=mysql" -e "MYSQL_USER=root" -e "MYSQL_DATABASE=fosit_ecommerce_store" -e ALLOW_EMPTY_PASSWORD=yes mysql:8.1.0
```


2. Run the pytest.
```bash
pytest -vv .
```
