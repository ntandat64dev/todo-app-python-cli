class GeneralError(Exception):
    def __init__(self, msg, trace=None):
        message = msg if msg else "Something went wrong."
        message = f"{message}\n{trace}" if trace else message
        super().__init__(message)


class InvalidArgument(Exception):
    def __init__(self, *invalid_args):
        message = f"Invalid argument(s): {', '.join(str(arg) for arg in invalid_args)}"
        super().__init__(message)


class UsernameNotFound(Exception):
    def __init__(self, username):
        message = (
            "Username not found" if not username else f"Username {username} not found"
        )
        super().__init__(message)


class UserNotFound(Exception):
    def __init__(self):
        message = "User not found"
        super().__init__(message)


class UserAlreadyExist(Exception):
    def __init__(self, username):
        message = (
            f"User {username} already exist!" if username else "User already exist!"
        )
        super().__init__(message)


class PasswordNotMatch(Exception):
    def __init__(self):
        message = "Password is wrong!"
        super().__init__(message)
