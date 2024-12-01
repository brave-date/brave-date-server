#Ensure the script is run as bash
SHELL:=/bin/bash

#Set help as the default for this makefile.
.DEFAULT: help

help:
	@echo "Please use 'make <target>' where <target> is one of:"
	@echo ""
	@echo "venv                     Create a virtual environment"
	@echo "install                  Install the package and all required core dependencies"
	@echo "run                      Running the app locally"
	@echo "clean                    Remove all build, test, coverage and Python artifacts"
	@echo "lint                     Check style with pre-commit"
	@echo "test                     Run tests quickly with pytest"
	@echo "test-all                 Run tests on every Python version with tox"
	@echo "build                    Build docker containers services"
	@echo "up                       Spin up the built containers"
	@echo "down                     Stop all running containers"

clean: clean-build clean-pyc clean-test

generate_dot_env:
	@if [[ ! -e .env ]]; then \
		cp .env.example .env; \
	fi

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

venv:
	@echo ""
	@echo "*** make virtual env ***"
	@echo ""
	(rm -rf .venv; uv venv -p 3.12 --python-preference managed; .  .venv/bin/activate;)
	@echo ""

lint:
	@echo ""
	@echo "*** Running formatters locally... ***"
	@echo ""
	@echo ""
	tox -ve lint
	@echo ""

test:
	@echo ""
	@echo "*** Running tests locally... ***"
	@echo ""
	@echo ""
	tox -e test
	@echo ""

test-all:
	@echo ""
	@echo "*** Running tests, formatters... ***"
	@echo ""
	@echo ""
	tox
	@echo ""

install: generate_dot_env
	@echo ""
	@echo "*** Generating a .env file and installing the required dependencies... ***"
	@echo ""
	@echo ""
	curl -LSf https://astral.sh/uv/install.sh | sh
	uv pip install -r pyproject.toml
	@echo ""

docker-run:
	@echo ""
	@echo "*** Running the app locally... ***"
	@echo ""
	@echo ""
	/root/.local/bin/poetry run server
	@echo ""

run:
	@echo ""
	@echo "*** Running the app locally... ***"
	@echo ""
	@echo ""
	uv run main.py
	@echo ""

dist: clean ## builds source and wheel package
	uv build

build:
	docker compose --file docker-compose.yml build

up:
	docker compose up

down:
	docker compose down

version-major:
	bump2version major

version-minor:
	bump2version minor
