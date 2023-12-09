from plantapop.shared.infrastructure.event.pika_event_bus import PikaEventBus


class AccountsEventBus(PikaEventBus):
    exchange_name = "accounts.user.events"
