class EntityNotFoundException(Exception):
    def __init__(self, repository, **kwargs):

        message = f"Entity with {kwargs} not found"
        super().__init__(message)
        self.repository = repository
        self.kwargs = kwargs
