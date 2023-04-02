.DEFAULT_GOAL := help

define HELP_COMMAND
Usage:
  make <command>

Commands:
  test                       Test this project using pytest.
  format                     Format the source code using black and isort.
  lint                       Runs the linting tool (mypy)
endef
export HELP_COMMAND

test:
	@coverage run -m pytest --html=tests/report/index.html . -v
	@coverage report -m
	@coverage html

format:
	@black aspreno
	@isort aspreno

lint:
	@mypy aspreno

help:
	@echo "$$HELP_COMMAND"
