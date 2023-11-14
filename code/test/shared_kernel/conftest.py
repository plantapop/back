try:
    from test.shared_kernel.fixtures import *  # noqa
except Exception:
    print("No database available: Only unittest can be run")
