try:
    from test.shared_kernel.fixtures import *  # noqa
except Exception as e:
    print(f"No database available: Only unittest can be run: {e}")
