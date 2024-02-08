USECASES_FOLDERS = [
    "application/",
    "domain/",
]

BOUNDED_CONTEXTS = [
    "accounts",
    "shared",
]

INJECTION_LINES = ["self.uow = ", "self.event_bus = "]

TYPES = [
    "= Type",
    "= TypeVar",
    "= Union",
]


def pre_mutation(context):

    # Load only test for bc
    if any(folder in context.filename for folder in BOUNDED_CONTEXTS):
        bc = next(folder for folder in BOUNDED_CONTEXTS if folder in context.filename)
        context.config.test_command = f"poetry run pytest -m 'unit and {bc}'"

    # Skip mutation if not inside unitest scope
    if not any(folder in context.filename for folder in USECASES_FOLDERS):
        context.skip = True
        return

    context_line = context.current_source_line.strip()

    # Skip if injection line (because unitest injects it)
    if any(line in context_line for line in INJECTION_LINES):
        context.skip = True
        return

    # Skip if type line (because not able to test types..)
    if any(typ in context_line for typ in TYPES):
        context.skip = True
        return
