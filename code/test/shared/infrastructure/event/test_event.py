import asyncio

import pytest
from sqlalchemy import select

from plantapop.shared.infrastructure.event.sqlalchemy_failover_event_bus import (
    SQLDomainEvent,
)


@pytest.mark.integration
async def test_publish(session, domain_event, event_bus):
    await event_bus.publish([domain_event])


@pytest.mark.integration
async def test_subscribe(session, domain_event, event_bus, subscriber):
    # When
    await event_bus.publish([domain_event])
    await asyncio.sleep(0.1)

    # Then
    assert await subscriber.cosas() == domain_event


@pytest.mark.integration
async def test_publish_error(session, domain_event, failed_event_bus):
    # When
    await failed_event_bus.publish([domain_event])
    await asyncio.sleep(0.1)
    query = await session.execute(select(SQLDomainEvent))
    # Then
    assert len(query.scalars().all()) == 1  # Clean DB in each test


@pytest.mark.integration
async def test_failover(session, domain_event, failed_event_bus, event_bus):
    # When
    await failed_event_bus.publish([domain_event])
    await asyncio.sleep(0.1)
    await event_bus.publish([domain_event])
    await asyncio.sleep(0.1)
    query = await session.execute(select(SQLDomainEvent))
    # Then
    assert len(query.scalars().all()) == 1


@pytest.mark.integration
async def test_subscriber_retry(session, domain_event, event_bus, failed_subscriber):
    # Given
    failed_subscriber = failed_subscriber(2)  # noqa todo, this may be afected by the max retries config
    await failed_subscriber.subscribe()

    # When
    await event_bus.publish([domain_event])
    await asyncio.sleep(0.2)

    # Then
    assert await failed_subscriber.cosas() == domain_event
    assert failed_subscriber.current_retries > 0


@pytest.mark.integration
async def test_subscriber_retry_dead_letter(
    session, domain_event, event_bus, failed_subscriber
):
    # Given
    failed_subscriber = failed_subscriber(90)  # noqa todo, this may be afected by the max retries config
    await failed_subscriber.subscribe()

    # When
    await event_bus.publish([domain_event])
    await asyncio.sleep(1)

    # Then
    assert await failed_subscriber.cosas() is None
    assert failed_subscriber.current_retries > 0
