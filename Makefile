PACKAGE := cliform
SRC_DIR = src/$(PACKAGE)
TESTS_MODULE = tests
TESTS_DIR = tests
DOC_DIR = docs

# Use current python binary instead of system default.
COVERAGE = python $(shell which coverage)
FLAKE8 = flake8

# Computed
PY_DIRS = $(SRC_DIR) $(TESTS_DIR)

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


test:
	python -W default manage_dev.py test

.PHONY: test testall


# Note: we run the linter in two runs, because our __init__.py files has specific warnings we want to exclude
lint:
	check-manifest
	$(FLAKE8) --config .flake8 --exclude $(PACKAGE)/__init__.py $(PACKAGE)
	$(FLAKE8) --config .flake8 --ignore F401 $(PACKAGE)/__init__.py

flake8:
	flake8 --config .flake8 $(SRC_DIR) $(TESTS_DIR)

isort:
	isort $(SRC_DIR) $(TESTS_DIR) --recursive --check-only --diff --project $(PACKAGE) --project $(TESTS_MODULE)

check-manifest:
	check-manifest

.PHONY: isort lint check-manifest flake8