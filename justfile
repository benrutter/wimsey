test:
    uv run pytest --cov=src --cov-fail-under=100 --cov-report=html
    uv run ty check src
    uv run ruff check src/**/*.py
    uv run ruff format src/**/*.py

build-docs:
    #!/usr/bin/env bash
    set -euo pipefail
    rm -rf wimsey-docs
    git clone ssh://git@codeberg.org/benrutter/wimsey-docs.git
    uv run zensical build
    cd wimsey-docs
    git config user.email "auto@generated.org"
    git config user.name "autogeneration"
    git add .
    git commit -m "Auto update of docs from Wimsey repo"
    git push
