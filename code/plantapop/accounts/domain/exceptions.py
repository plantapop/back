class UserAlreadyExistsException(Exception):
    pass


class EmailAlreadyExistsException(Exception):
    pass


class UserNotFoundException(Exception):
    pass


class InvalidPasswordException(Exception):
    pass
