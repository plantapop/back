import sys

import pytest
import toml
from sqlalchemy.ext.asyncio import AsyncEngine

from plantapop.shared.infrastructure.repository.database import engine
from plantapop.shared.infrastructure.repository.models import get_base

mark = sys.argv[-1]


async def init_models(engine: AsyncEngine = engine):
    Base = get_base()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


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
