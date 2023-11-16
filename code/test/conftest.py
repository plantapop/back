import pytest
import toml

try:
    from test.shared.fixtures import client, session  # noqa
except Exception as e:
    print(f"No database available: Only unittest can be run: {e}")


@pytest.fixture()
def app_version():
    """Get App version from pyproject.toml"""

    with open("pyproject.toml", "r") as f:
        pyproject = toml.load(f)
    return pyproject["tool"]["poetry"]["version"]
