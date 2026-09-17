.DEFAULT_GOAL := help
PYTHON ?= python3
CREDS ?= .creds
BUILD_FLAGS ?=
VERBOSE ?= 0

.PHONY: help install-dev test lint check build check-dist publish-testpypi publish-pypi clean

help:
	@printf '%s\n' \
	  'make install-dev      Install project and development/release tools' \
	  'make test             Run offline regression tests' \
	  'make lint             Run pylint (minimum score 9.5)' \
	  'make check            Run tests and lint' \
	  'make build            Build wheel and source archive, then validate' \
	  'make check-dist       Validate existing release archives' \
	  'make publish-testpypi Upload existing archives to TestPyPI' \
	  'make publish-pypi     Upload existing archives to PyPI' \
	  'make clean            Remove generated build artifacts' \
	  'Overrides: PYTHON=python3 CREDS=.creds BUILD_FLAGS=--no-isolation VERBOSE=1'

install-dev:
	$(PYTHON) -m pip install -e '.[dev]'

test:
	$(PYTHON) -m unittest discover -s tests -v

lint:
	$(PYTHON) -m pylint --fail-under=9.5 itopcli_app/cli.py itopcli

check: test lint

build:
	$(PYTHON) -m build $(BUILD_FLAGS)
	$(MAKE) check-dist PYTHON="$(PYTHON)"

check-dist:
	$(PYTHON) scripts/check_dist.py
	$(PYTHON) -m twine check --strict dist/*

publish-testpypi: check-dist
	@$(PYTHON) scripts/publish.py testpypi --creds "$(CREDS)" $(if $(filter 1,$(VERBOSE)),--verbose,)

publish-pypi: check-dist
	@$(PYTHON) scripts/publish.py pypi --creds "$(CREDS)" $(if $(filter 1,$(VERBOSE)),--verbose,)

clean:
	rm -rf build dist itopcli.egg-info
