try:
    from test.shared_kernel.fixtures import app_version, client, session  # noqa

    __all__ = [
        "session",
        "client",
        "app_version",
    ]
except Exception as e:
    print(f"No database available: Only unittest can be run: {e}")
