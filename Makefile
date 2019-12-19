PACKAGE := cliform
SRC_DIR = src/$(PACKAGE)
TESTS_MODULE = tests
TESTS_DIR = tests
DEMO_DIR = demo
DOC_DIR = docs

# Use current python binary instead of system default.
COVERAGE = python $(shell which coverage)
FLAKE8 = flake8
MYPY = mypy

# Computed
PY_DIRS = $(SRC_DIR) $(TESTS_DIR) $(DEMO_DIR)

all: default


default:

doc:
	$(MAKE) -C $(DOC_DIR) html

.PHONY: all default doc

clean:
	find $(PY_DIRS) -type f -name '*.pyc' -delete
	find $(PY_DIRS) -type f -path '*/__pycache__/*' -delete
	find $(PY_DIRS) -type d -empty -delete


update:
	pip install --upgrade pip setuptools
	pip install --upgrade -r requirements_dev.txt
	pip freeze

release:
	fullrelease

.PHONY: default clean update release


testall:
	tox

mypy:
	$(MYPY) $(SRC_DIR) $(TESTS_DIR) $(DEMO_DIR)

test:
	python -W default manage_dev.py test

.PHONY: mypy test testall


lint: check-manifest isort flake8

flake8:
	flake8 --config .flake8 $(SRC_DIR) $(TESTS_DIR) $(DEMO_DIR) setup.py

isort:
	isort $(SRC_DIR) $(TESTS_DIR) --recursive --check-only --diff --project $(PACKAGE) --project $(TESTS_MODULE) --project $(DEMO_DIR)

check-manifest:
	check-manifest

.PHONY: isort lint check-manifest flake8
