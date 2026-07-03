"""Creates markdown datacatalogue from example file."""
import json
import textwrap
from typing import Any

import yaml


def _indent(text: str) -> str:
    return textwrap.indent(text, "    ")

with open("tests/example-passing.yaml") as file:
    contents = yaml.safe_load(file.read())

catalogue = """---
icon: lucide/book-marked
---

# Test Catalogue

Below is a full list of all available tests within Wimsey.
"""

NEWLINE = "\n"


def _stringify(x: Any) -> Any:
    try:
        float(x)
        return x
    except ValueError:
        return f'"{x}"'
    except Exception:
        return x


for test in contents:
    description = test.pop("description")
    args = (NEWLINE + "    ").join(
        [f"{k}={_stringify(v)}," for k, v in test.items() if k != "test"]
    )
    yaml_tab = _indent(f'```yaml\n{yaml.dump(test)}```')
    json_tab = _indent(f'```yaml\n{json.dumps(test, indent=2)}\n```')
    python_tab = _indent(
        f'```python\n'
        f'from wimsey.tests import {test["test"]}\n\n'
        f'my_test = {test["test"]}(\n'
        f'    {args}\n'
        f')\n'
        f'```'
    )
    catalogue += f"""
# {test["test"]}

{description}

=== "yaml"

{yaml_tab}

=== "json"

{json_tab}

=== "python"

{python_tab}

"""

with open("docs/test-catalogue.md", "w") as file:
    file.write(catalogue)
