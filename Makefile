override SHELL := /bin/sh
override .SHELLFLAGS := -c
ifneq ($(strip $(MAKEFILES)),)
$(error MAKEFILES must not be set)
endif
override MAKEFILES :=
ifneq ($(origin MAKEFILE_LIST),file)
$(error MAKEFILE_LIST must not be overridden)
endif
override ROOT := $(shell MAKEFILE_LIST_RAW='$(subst ','"'"',$(MAKEFILE_LIST))' python3 -c "import os; raw = os.environ['MAKEFILE_LIST_RAW']; candidates = [raw] + [raw[index + 1:] for index, char in enumerate(raw) if char == ' ']; path = next((candidate for candidate in candidates if (candidate == 'Makefile' or candidate.endswith('/Makefile')) and os.path.isfile(os.path.abspath(candidate))), None); assert path is not None, 'trusted Makefile path not found'; print(os.path.dirname(os.path.abspath(path)))")

.PHONY: build check lint static-check test verify

override PYTHON := python3
build check lint static-check test verify: override ROOT := $(ROOT)
build check lint static-check test verify: override PYTHON := $(PYTHON)

check: verify

verify: static-check test

lint build: static-check

test:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) "$(ROOT)/scripts/test-check-baseline.py"
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) "$(ROOT)/scripts/test-artifact-ownership-mutations.py"

static-check:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) "$(ROOT)/scripts/check-baseline.py"
