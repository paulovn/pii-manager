#  Manage package tasks
#  -----------------------------------
#  make pkg       -> build the package
#  make unit      -> perform unit tests
#  make install   -> install the package in a virtualenv
#  make uninstall -> uninstall the package from the virtualenv

# Package name
NAME := text-anonymizer

# Virtualenv to install in. In this order:
#   1. the one given by the VENV environment variable
#   2. an active one (as given by the VIRTUAL_ENV environment variable)
#   3. a default
VENV ?= $(shell echo $${VIRTUAL_ENV:-/opt/venv/bigscience})

PYTHON ?= python3

# --------------------------------------------------------------------------

# Package version: taken from the __init__.py file
VERSION_FILE := src/text_anonymizer/__init__.py
VERSION	     := $(shell grep VERSION $(VERSION_FILE) | sed -r "s/VERSION = '(.*)'/\1/")

PKGFILE := dist/$(NAME)-$(VERSION).tar.gz

# --------------------------------------------------------------------------

all:

build pkg: $(PKGFILE)

version:
	@echo $(VERSION)

clean:
	rm -f $(PKGFILE)

unit:
	PYTHONPATH=src:test pytest $(ARGS) test/unit 

rebuild: clean build


# --------------------------------------------------------------------------

$(PKGFILE): $(VERSION_FILE) setup.py
	$(PYTHON) setup.py sdist

$(VENV):
	$(PYTHON) -m venv $@
	$@/bin/pip install -r requirements.txt

install:
	$(VENV)/bin/pip install $(PKGFILE)

uninstall:
	$(VENV)/bin/pip uninstall -y $(NAME)

reinstall: uninstall clean pkg install
