# Lists all available commands.
default:
    @just --list

# Creates .venv and installs requirements.txt.
setup:
    @(\
        python -m venv .venv && \
        source .venv/bin/activate &&  \
        pip3 install -U pip && \
        pip3 install -r requirements.txt \
    )

# Upgrades and recompiles requirements.txt from requirements.in.
pip-update:
    @pip-compile -U requirements.in --output-file requirements.txt

# Builds the sdist and wheel.
build:
    @python -m build

# Uploads the built dist to PyPI.
publish:
    @twine upload dist/*

# Deploys docs to GitHub Pages.
deploy-docs:
    @mkdocs gh-deploy

# Serves docs locally for preview.
serve-docs:
    @mkdocs serve

# Runs pytest inside .venv.
test:
    @(\
        source .venv/bin/activate && \
        pytest \
    )
