VIRTUALENV = virtualenv
VENV := $(shell echo $${VIRTUAL_ENV-$$PWD/.venv})
PYTHON = $(VENV)/bin/python
DEV_STAMP = $(VENV)/.dev_env_installed.stamp
INSTALL_STAMP = $(VENV)/.install.stamp
TEMPDIR := $(shell mktemp -d)

.PHONY: virtualenv

OBJECTS = .venv
SERVER = https://kinto-ota.dev.mozaws.net/v1/

build: $(PYTHON)
$(PYTHON):
	virtualenv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt

sync:
	$(PYTHON) switchboard2kinto.py --auth $(AUTH) -s $(SERVER)
