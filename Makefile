PACKAGE := cliform
SRC_DIR = src/$(PACKAGE)
TESTS_MODULE = tests
TESTS_DIR = tests
DEMO_DIR = demo
DOC_DIR = docs

# Use current python binary instead of system default.
COVERAGE = python coverage
FLAKE8 = flake8
MYPY = mypy
MANAGE_PY = manage_dev.py

# Sentinel files
SENTINEL_DEPS = .build.deps
SENTINEL_MYPY = .build.mypy
SENTINEL_TEST = .build.test
SENTINEL_FLAKE8 = .build.flake8
SENTINEL_ISORT = .build.isort

# Computed
PY_DIRS = $(SRC_DIR) $(TESTS_DIR) $(DEMO_DIR)
PY_FILES = $(shell find $(PY_DIRS) -type f -name '*.py') $(MANAGE_PY) setup.py

all: default


default:

doc:
	$(MAKE) -C $(DOC_DIR) html

.PHONY: all default doc

clean:
	find $(PY_DIRS) -type f -name '*.pyc' -delete
	find $(PY_DIRS) -type f -path '*/__pycache__/*' -delete
	find $(PY_DIRS) -type d -empty -delete


update: $(SENTINEL_DEPS)

force-update:
	rm -f $(SENTINEL_DEPS)
	$(MAKE) update

$(SENTINEL_DEPS): requirements_dev.txt
	pip install --upgrade pip setuptools
	pip install --upgrade -r requirements_dev.txt
	pip freeze
	touch $(SENTINEL_DEPS)

release:
	fullrelease

.PHONY: default clean force-update update release


testall:
	tox

mypy: $(SENTINEL_MYPY)

$(SENTINEL_MYPY): setup.cfg $(PY_FILES)
	$(MYPY) $(SRC_DIR) $(TESTS_DIR) $(DEMO_DIR)
	touch $@

test: $(SENTINEL_TEST)

$(SENTINEL_TEST): $(SENTINEL_DEPS) $(PY_FILES)
	python -W default $(MANAGE_PY) test
	touch $@

.PHONY: mypy test testall


lint: check-manifest isort flake8

flake8: $(SENTINEL_FLAKE8)

$(SENTINEL_FLAKE8): $(SENTINEL_DEPS) $(PY_FILES) .flake8
	flake8 --config .flake8 $(SRC_DIR) $(TESTS_DIR) $(DEMO_DIR) setup.py
	touch $@

isort: $(SENTINEL_ISORT)

$(SENTINEL_ISORT): $(SENTINEL_DEPS) $(PY_FILES)
	isort $(SRC_DIR) $(TESTS_DIR) --recursive --check-only --diff --project $(PACKAGE) --project $(TESTS_MODULE) --project $(DEMO_DIR)
	touch $@

check-manifest:
	check-manifest

.PHONY: isort lint check-manifest flake8
