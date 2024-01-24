USECASES_FOLDERS = [
    "application",
    "domain",
]


def pre_mutation(context):
    if not any(folder in context.filename for folder in USECASES_FOLDERS):
        context.skip = True
