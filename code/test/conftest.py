import sys

import pytest
import toml

mark = sys.argv[-1]


if mark == "integration":
    from test.integration_fixtures import *  # noqa

if mark == "acceptance":
    from test.acceptance_fixtures import *  # noqa

if mark == "unit":
    from test.unit_fixtures import *  # noqa


@pytest.fixture()
def app_version():
    """Get App version from pyproject.toml"""

    with open("pyproject.toml", "r") as f:
        pyproject = toml.load(f)
    return pyproject["tool"]["poetry"]["version"]
