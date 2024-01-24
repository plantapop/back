USECASES_FOLDERS = [
    "application/",
    "domain/",
]

INJECTION_LINES = ["self.uow = ", "self.event_bus = "]


def pre_mutation(context):
    if not any(folder in context.filename for folder in USECASES_FOLDERS):
        context.skip = True
        return
    context_line = context.current_source_line.strip()
    if any(line in context_line for line in INJECTION_LINES):
        context.skip = True
        return
