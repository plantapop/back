import asyncio

import pytest


@pytest.mark.integration
async def test_publish(domain_event, event_bus):
    await event_bus.publish([domain_event])


@pytest.mark.integration
@pytest.mark.asyncio
async def test_subscribe(domain_event, event_bus, subscriber):
    await event_bus.publish([domain_event])
    await asyncio.sleep(0.5)
    assert await subscriber.cosas() == 1
