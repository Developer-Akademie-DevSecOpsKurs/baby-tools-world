# Baby Tools World

This repository contains the source code of the 'Baby Tools World' which is a simple full stack shop application written in Python using Django 5.
The project was developed for educational purposes only and therefore has no claim to feature completeness, or only minimal claims regarding application security, user experience, or design.

> [!NOTE]
> This project assumes you already know the python programming language

## Prerequisites

In order to seamlessly interact with the repository and the software it contains you need to following tools preinstalled:

- Python Interpreter
- OCI-Compliant Container Engine (e.g. podman, docker, etc.)
- Editor/IDE of your choice (VSC, PyCharm, etc.)

## Quickstart

In order to quickly get started with the project follow these steps:

1. clone the repository
1. nagivate to the repository
1. (optional) create a virtual environment with `python -m venv my-venv`
    1. activate the virtual environment: 
        - on Windows run: `my-venv/Scripts/activate`
        - on MacOS/Linux run: `source my-venv/bin/activate`
1. install the project dependencies with `pip install -r requirements.txt`
1. configure required application environment variables
    - `cp example.env .env`
1. prepare the database (create and apply migrations)
    1. `python manage.py makemigrations`
    1. `python manage.py migrate`
1. start the application with `python manage.py runserver`
1. verify the application is running by visiting `localhost:8000`
1. (optional) create a superuser by running: `python manage.py createsuperuser`

## Project Structure

- `.gitlab`: GitLab specific project files
- `.github`: GitHub specific project files
- `src`: application source code, containing the django project, apps, and other files
- `requirements.txt`: the project dependencies

### Apps Overview

The project is modularized into several apps:

- `products`: Manages product listings and categories
- `users`: Handles user authentication and registration.

Each app has its own `models.py`, `views.py`, `urls.py`, and `admin.py` files to encapsulate its functionality.


## Usage

In this section you can read about the project a bit more in detail.

### Configuration

To configure the project, follow these steps:

1. Copy the example environment file to the `src` directory: `cp example.env src/.env`.
    - the file needs to be stored next to the manage.py file in order to function properly. 
    Other locations might also work but there is no guarantuee, and in last consequence you will need to update to project correspondingly.
2. Open your `src/.env` and set the required environment variables:
    - `ALLOWED_HOSTS`: provide a list of comma-separated values for the allowed host configuration => Defaults to `'localhost, 127.0.0.1, 0.0.0.0'`
    - `DEBUG`: Set to `True` for development or `False` for production. Defaults to `True`

### Testing

This project contains tests for the corresponding apps in the respective packages.
Tests in Django can either be located in a `tests.py` file within a django-app, or you could also have a module named `tests` (essentially a folder with an `__init__.py` file).

> [!TIP]
> The django testrunner will by default discover tests by finding all python files that contain the word `test` in their name, e.g. `test.py`, `test_model.py`, or similar.

Example Structure:

```console
baby-tool-world/src/products
├───management
├───migrations
├───templates
└───tests <-- this is the module
      ├───__init__.py
      ├───test_category_model.py <-- this is a test file
      └───test_category_model.py <-- this is a test file too
```

#### Running tests

To run the tests with the `django testrunner` you can use the following command:

- `python manage.py test`, you need to run this in the folder where `manage.py` lives -> `src`

For more information about testing, refer to the testing documentation in this repository, see [here](./docs/testing.md)

### Running with a WSGI Server

**WSGI** (Web Server Gateway Interface) is a specification that defines a standard interface between web servers and Python web applications or frameworks.
It acts as a bridge, allowing web servers to communicate with Python applications in a consistent manner.

In Django deployments, WSGI is used to serve the application in a production environment. 
It enables the web server (e.g., Gunicorn, uWSGI, or Apache with mod_wsgi) to forward 
requests to the Django application and return responses to the client. This ensures that 
the application can handle HTTP requests efficiently and reliably in a scalable setup.

> `gunicorn` and `waitress` are similar tools and can be used for the same purpose,
> but sometimes running `gunicorn` on windows results in problems that can be circumvented by using `waitress` instead.
>
> See the following [quote](https://docs.gunicorn.org/en/stable/index.html) from the official gunicorn website:
>> Gunicorn ‘Green Unicorn’ is a Python WSGI HTTP Server for UNIX.

For more information about WSGI and its configuration, see the [wsgi documentation](./docs/wsgi.md).

### Seeding the application with data

This section will guide you through the process of providing an initial seed to the application.

To initially seed the application you can run the management command `seed_db` to fill the database with some categories and testing products.

In order to run that comand go the the directory, where your `manage.py` file is stored and run the following command:

```bash
python manage.py seed_db
```
