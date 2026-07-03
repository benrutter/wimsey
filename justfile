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
