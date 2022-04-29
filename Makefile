SHELL := /bin/bash

setup:
	@(\
		python -m venv .venv && \
		source .venv/bin/activate &&  \
		pip3 install -U pip && \
		pip3 install -r requirements.txt \
	)

pip-update:
	@pip-compile -U requirements.in --output-file requirements.txt

build:
	@python -m build

publish:
	@twine upload dist/*

deploy-docs:
	@mkdocs gh-deploy

serve-docs:
	@mkdocs serve

test:
	@(\
		source .venv/bin/activate && \
		pytest \
	)
