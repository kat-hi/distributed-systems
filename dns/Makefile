.ONESHELL:

compile:
	@ echo "make venv: handles the installation for you (maybe)"
	@ echo "make run zone=\"beuth-hochschule.de\": runs the script"

VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3

venv:
	virtualenv -p python3 venv
	$(VENV_NAME)/bin/activate
	${PYTHON} -m pip install dnspython	

run: venv
	@ ${PYTHON} DnsChecker.py $(zone)
