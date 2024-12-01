# Brave Date Server

<div align="center">

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Static typing: mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/brave-date/brave-date-server/main.svg)](https://results.pre-commit.ci/latest/github/brave-date/brave-date-server/main)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
![Codeql](https://github.com/github/docs/actions/workflows/codeql.yml/badge.svg)

</div>

[![Architecture](https://github.com/brave-date/brave-date/blob/docs/docs/static/images/architecture.png)](https://github.com/brave-date/brave-date-server)

A Fully Async-based backend for [Brave Date](https://github.com/brave-date/brave-date).

## Table of Contents

- [Database](#database)
- [Development Requirements](#development-requirements)
- [Project Structure](#project-structure)
- [Installation with Make](#installation-with-make)
- [Access Swagger Documentation](#access-swagger-documentation)
- [Access Redocs Documentation](#access-redocs-documentation)
- [Deployments](#deployments)
- [Core Dependencies](#core-dependencies)
- [License](#license)

## Database

[![Brave Date Database Collections](https://brave-date.github.io/brave-date/static/images/collections.png)](https://brave-date.github.io/brave-date/data-models)

You can refer to the official documentation for detailed information about [the database collections](https://docs.brave-date.wiseai.dev/data-models) and how data was modeled.

## Development Requirements

- Make (GNU command)
- Python (>= 3.12)
- UV (>= 0.5)

If you don't have Python installed yet, it is recommended to use [uv](https://github.com/astral-sh/uv) to manage your Python versions and virtual environments.

## Project Structure

<details>
<summary><code>❯ tree app</code></summary>

```sh
.
├── auth          # Package contains different config files for the `auth` app.
│   ├── crud.py       # Module contains different CRUD operations performed on the database.
│   ├── models.py     # Module contains different data models for ODM to interact with database.
│   ├── router.py     # Module contains different routes for this api.
│   └── schemas.py    # Module contains different schemas for this api for validation purposes.
├── matches       # Package contains different config files for the `matches` app.
│   ├── crud.py       # Module contains different CRUD operations performed on the database.
│   ├── models.py     # Module contains different models for ODMs to inteact with database.
│   ├── router.py     # Module contains different routes for this api.
│   └── schemas.py    # Module contains different schemas for this api for validation purposes.
├── messages      # Package contains different config files for the `messages` app.
│   ├── crud.py       # Module contains different CRUD operations performed on the database.
│   ├── models.py     # Module contains different models for ODMs to inteact with database.
│   ├── router.py     # Module contains different routes for this api.
│   └── schemas.py    # Module contains different schemas for this api for validation purposes.
├── users         # Package contains different config files for the `users` app.
│   ├── crud.py       # Module contains different CRUD operations performed on the database.
│   ├── models.py     # Module contains different models for ODMs to inteact with database.
│   ├── router.py     # Module contains different routes for this api.
│   └── schemas.py    # Module contains different schemas for this api for validation purposes.
├── websockets    # Package contains different config files for the `websockets` app.
│   ├── manager.py    # Module contains the manager class definitions.
│   ├── router.py     # Module contains different routes for this api.
├── utils         # Package contains different common utility modules for the whole project.
│   ├── crypt.py
│   ├── dependencies.py     # A utility script that yield a session for each request to make the crud call work.
│   ├── engine.py           # A utility script that initializes an ODMantic engine and client and set them as app state variables.
│   ├── jwt.py              # A utility script for JWT.
│   ├── mixins.py           # A utility script that contains common mixins for different models.
├── config.py     # Module contains the main configuration settings for project.
├── __init__.py
├── main.py       # Startup script. Starts uvicorn.
└── py.typed      # mypy related file.
```

</details>

## Installation with Make

The best way to configure, install main dependencies, and run the project is by using `make`. So, ensure you have `make` installed and configured on your machine. If it is not the case, head over to [this thread](https://stackoverflow.com/questions/32127524/how-to-install-and-use-make-in-windows) on StackOverflow to install it on windows, or [this thread](https://stackoverflow.com/questions/11494522/installing-make-on-mac) to install it on Mac OS.

Having `make` installed and configured on your machine, you can now run `make` under the root directory of this project to explore different available commands to run:

```sh
make

Please use 'make <target>' where <target> is one of:

venv                     Create a virtual environment
install                  Install the package and all required core dependencies
run                      Running the app locally
clean                    Remove all build, test, coverage and Python artifacts
lint                     Check style with pre-commit
test                     Run tests quickly with pytest
test-all                 Run tests on every Python version with tox
coverage                 Check code coverage quickly with the default Python
build                    Build docker containers services
up                       Spin up the containers
down                     Stop all running containers
```

### 1. Create a virtualenv

```sh
make venv
```

### 2. Activate the virtualenv

```sh
source .venv/bin/activate
```

### 3. Install dependencies

```sh
make install
```

**Note**: _This command will automatically generate a `.env` file from `.env.example`, uninstall the old version of poetry on your machine, then install latest version `1.2.2`, and install the required main dependencies._

### 4. Setup a MongoDB Atlas account

Head over to [the official website](https://www.mongodb.com/cloud/atlas/signup) to create a MongoDB account and a cluster.

### 5. Set your MongoDB Credentials

Fill in the following environment variables in your .env file accordingly:

```yaml
# Database
MONGODB_USERNAME=
MONGODB_PASSWORD=
MONGODB_HOST=cluster_name.example.mongodb.net
MONGODB_DATABASE=tinder
```

### 6. Create a Pinata Cloud Account

Create a free account on [Pinata Cloud](https://www.pinata.cloud/) and set up your API key by creating a new API key in your account dashboard.

### 7. Set your Pinata Cloud API Key and Secret

Set the following environment variables in your `.env` file according to the API key and secret from your Pinata Cloud account:

```yaml
# Pinata Cloud
PINATA_API_KEY=
PINATA_API_SECRET=
```

### 8. Generate a secret key

Generate a secret key using OpenSSL and update its env var in the .env file.

```sh
openssl rand -hex 128

afa1639545d53ecf83c9f8acf4704abe1382f9a9dbf76d2fd229d4795a4748712dbfe7cf1f0a812f1c0fad2d47c8343cd1017b22fc3bf43d052307137f6ba68cd2cb69748b561df846873a6257e3569d6307a7e022b82b79cb3d6e0fee00553d80913c1dcf946e2e91e1dfcbba1ed9f34c9250597c1f70f572744e91c68cbe76
```

```yaml
# App config:
JWT_SECRET_KEY=afa1639545d53ecf83c9f8acf4704abe1382f9a9dbf76d2fd229d4795a4748712dbfe7cf1f0a812f1c0fad2d47c8343cd1017b22fc3bf43d052307137f6ba68cd2cb69748b561df846873a6257e3569d6307a7e022b82b79cb3d6e0fee00553d80913c1dcf946e2e91e1dfcbba1ed9f34c9250597c1f70f572744e91c68cbe76
DEBUG=info
```

### 9. Run The Project Locally

```sh
make run
```

**Note**: _You have to set **DEBUG=info** to access the docs._

## Access Swagger Documentation

> <http://localhost:8000/docs>

## Access Redocs Documentation

> <http://localhost:8000/redocs>

## Deployments

### Deploy locally with Compose v2

First thing first, to run the entire platform, you have to clone the `brave-date` submodule using the following command:

```sh
git submodule update --init --recursive
```

Once that is done, make sure you have [compose v2](https://github.com/docker/compose) installed and configured on your machine, and run the following command to build the predefined docker services(make sure you have a .env file beforehand):

**Using Make**

```sh
make build
```

or simply running:

```
docker compose build
```

Once that is done, you can spin up the containers:

**Using Make**

```sh
make up
```

or running:

```
docker compose up
```

Wait until the client service becomes available:

```sg
brave-date-client-1      | Starting the development server...
```

You can stop the running containers but issuing the following command on a separate terminal session:

```
make down
```

### Heroku

This button will only deploy the server.

[![Deploy on Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/brave-date/brave-date-server)

#### Heroku CLI (Experimental: Deploy the entire stack)

Note that this approach is not perfect because in the docker world, you should only have one service for each container, and you should use docker-compose to build and run more than two containers(e.g. one for the server and the other one for the client). However, Heroku doesn't support docker-compose with multiple services(except databases and such.). Hence running both services in one container.

To do so, ensure you have already installed and configured the Heroku CLI on your machine. If it is not the case, you can install it on Ubuntu using the following command:

```sh
sudo wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh
```

Now, you need to install the Heroku container registry plugin:

```sh
heroku plugins:install heroku-container-registry
```

Once that is completed, log in to your registry:

```sh
heroku container:login
```

Now, create a Heroku app:

```sh
heroku create <a unique app name>
```

You can list all your apps to verify that your recent app has been created:

```sh
heroku apps
```

Set your env variables in the `.env` file.

Build your container image:

```sh
docker compose -f heroku-compose.yml build
```

Deploy to Heroku:

```sh
heroku container:push web --app <your heroku app name>; heroku logs --tail
```

Once the build and push are completed, you can run the following command in a separate shell to interact with the app:

```sh
heroku open --app=<your app name>
```

You can refer to [heroku dev center](https://devcenter.heroku.com/articles/local-development-with-docker-compose) for more info. Happy Herokuing!


## Core Dependencies

The following packages are the main dependencies used to build this project:

- [`python`](https://github.com/python/cpython)
- [`fastapi`](https://github.com/tiangolo/fastapi)
- [`uvicorn`](https://github.com/encode/uvicorn)
- [`pydantic`](https://github.com/pydantic/pydantic)
- [`odmantic`](https://github.com/art049/odmantic)
- [`PyJWT`](https://github.com/jpadilla/pyjwt)
- [`passlib`](https://passlib.readthedocs.io/en/stable/index.html)
- [`python-multipart`](https://github.com/andrew-d/python-multipart)

## License

This project and the accompanying materials are made available under the terms and conditions of the [`MIT LICENSE`](https://github.com/brave-date/brave-date-server/blob/main/LICENSE).
