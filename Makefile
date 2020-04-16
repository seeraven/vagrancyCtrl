# ----------------------------------------------------------------------------
# Makefile for vargancyCtrl
#
# Copyright (c) 2020 by Clemens Rabe <clemens.rabe@clemensrabe.de>
# All rights reserved.
# This file is part of vagrancyCtrl (https://github.com/seeraven/vagrancyCtrl)
# and is released under the "BSD 3-Clause License". Please see the LICENSE file
# that is included as part of this package.
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
#  SETTINGS
# ----------------------------------------------------------------------------

SHELL               = /bin/bash
PYLINT_RCFILE      := $(PWD)/.pylintrc
PYCODESTYLE_CONFIG := $(PWD)/.pycodestyle

MODULES            := vagrancy
SCRIPTS            := vagrancyCtrl
MODULES_ABS        := $(patsubst %,$(PWD)/%,$(MODULES))
SCRIPTS_ABS        := $(patsubst %,$(PWD)/%,$(SCRIPTS))
PYTHONPATH         := $(PWD)                             # $(subst $(eval) ,:,$(MODULES_ABS))
SOURCES            := $(SCRIPTS_ABS) $(MODULES_ABS)
UNITTEST_DIR       := tests/unittests
UNITTEST_FILES     := $(shell find $(UNITTEST_DIR) -name '*.py')


# ----------------------------------------------------------------------------
#  DEFAULT TARGETS
# ----------------------------------------------------------------------------

.PHONY: help system-setup venv-bash check-style pylint pycodestyle flake8 unittests unittests-coverage apidoc doc man test clean

all:	check-style.venv unittests.venv


# ----------------------------------------------------------------------------
#  USAGE
# ----------------------------------------------------------------------------
help:
	@echo "Makefile for vagrancyCtrl"
	@echo "========================="
	@echo
	@echo "Targets for Style Checking in venv:"
	@echo " check-style.venv : Call pylint, pycodestyle and flake8"
	@echo " pylint.venv      : Call pylint on the source files."
	@echo " pycodestyle.venv : Call pycodestyle on the source files."
	@echo " flake8.venv      : Call flake8 on the source files."
	@echo
	@echo "Targets for Style Checking in System Environment:"
	@echo " check-style      : Call pylint, pycodestyle and flake8"
	@echo " pylint           : Call pylint on the source files."
	@echo " pycodestyle      : Call pycodestyle on the source files."
	@echo " flake8           : Call flake8 on the source files."
	@echo
	@echo "Targets for Functional Tests in local DMD setup:"
	@echo " test.dlang       : Execute the functional tests."
	@echo
	@echo "Targets for Functional Tests in System Environment:"
	@echo " test             : Execute the functional tests."
	@echo
	@echo "venv Setup:"
	@echo " venv             : Create the venv."
	@echo " venv-bash        : Start a new shell in the venv for debugging."
	@echo
	@echo "Misc Targets:"
	@echo " system-setup     : Install all dependencies in the currently"
	@echo "                    active environment (system or venv)."
	@echo " clean            : Remove all temporary files."
	@echo
	@echo "Development Information:"
	@echo " MODULES    = $(MODULES)"
	@echo " SCRIPTS    = $(SCRIPTS)"
	@echo " PYTHONPATH = $(PYTHONPATH)"
	@echo " SOURCES    = $(SOURCES)"


# ----------------------------------------------------------------------------
#  SYSTEM SETUP
# ----------------------------------------------------------------------------

system-setup:
	@echo "-------------------------------------------------------------"
	@echo "Installing pip..."
	@echo "-------------------------------------------------------------"
	@pip install -U pip
	@echo "-------------------------------------------------------------"
	@echo "Installing package requirements..."
	@echo "-------------------------------------------------------------"
	@pip install -r requirements.txt
	@echo "-------------------------------------------------------------"
	@echo "Installing package development requirements..."
	@echo "-------------------------------------------------------------"
	@pip install -r dev_requirements.txt


# ----------------------------------------------------------------------------
#  VENV SUPPORT
# ----------------------------------------------------------------------------

venv:
	@if [ ! -d venv ]; then python3 -m venv venv; fi
	@source venv/bin/activate; \
	make system-setup
	@echo "-------------------------------------------------------------"
	@echo "Virtualenv venv setup. Call"
	@echo "  source venv/bin/activate"
	@echo "to activate it."
	@echo "-------------------------------------------------------------"


venv-bash: venv
	@echo "Entering a new shell using the venv setup:"
	@source venv/bin/activate; \
	/bin/bash
	@echo "Leaving sandbox shell."


%.venv: venv
	@source venv/bin/activate; \
	make $*


# ----------------------------------------------------------------------------
#  STYLE CHECKING
# ----------------------------------------------------------------------------

check-style: pylint pycodestyle flake8

pylint:
	@pylint --rcfile=$(PYLINT_RCFILE) $(SOURCES) $(UNITTEST_FILES)
	@echo "pylint found no errors."


pycodestyle:
	@pycodestyle --config=$(PYCODESTYLE_CONFIG) $(SOURCES) $(UNITTEST_DIR)
	@echo "pycodestyle found no errors."


flake8:
	@flake8 $(SOURCES) $(UNITTEST_DIR)
	@echo "flake8 found no errors."


# ----------------------------------------------------------------------------
#  UNIT TESTS
# ----------------------------------------------------------------------------

unittests:
	@PYTHONPATH=$(PYTHONPATH) nosetests -v -w tests/unittests

unittests-coverage:
	@rm -rf doc/coverage
	@mkdir -p doc/coverage
	@PYTHONPATH=$(PYTHONPATH) nosetests -v -w tests/unittests --with-coverage \
        --cover-package=vagrancy --cover-erase --cover-min-percentage=80 \
        --cover-branches \
        --cover-html --cover-html-dir=../../doc/coverage \
        --cover-xml  --cover-xml-file=../../doc/coverage/coverage.xml


# ----------------------------------------------------------------------------
#  FUNCTIONAL TESTS
# ----------------------------------------------------------------------------

test:
	@test/run_tests.sh


# ----------------------------------------------------------------------------
#  DOCUMENTATION
# ----------------------------------------------------------------------------

apidoc:
	@rm -rf doc/source/apidoc
	@PYTHONPATH=$(PYTHONPATH) sphinx-apidoc -f -M -T -o doc/source/apidoc $(MODULES)

doc: apidoc
	@PYTHONPATH=$(PYTHONPATH) sphinx-build -W -b html doc/source doc/build

man:
	@PYTHONPATH=$(PYTHONPATH) sphinx-build -W -b man doc/manpage doc/build


# ----------------------------------------------------------------------------
#  MAINTENANCE TARGETS
# ----------------------------------------------------------------------------

clean:
	@rm -rf venv doc/coverage doc/build doc/source/apidoc .coverage
	@find . -name "__pycache__" -exec rm -rf {} \; 2>/dev/null || true
	@find . -iname "*~" -exec rm -f {} \;
	@find . -iname "*.pyc" -exec rm -f {} \;

