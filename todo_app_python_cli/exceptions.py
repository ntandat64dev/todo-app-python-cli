from enum import Enum


class ExceptionLevel(Enum):
    INFO = 0
    ERROR = 1


class AppException(Exception):
    def __init__(self, message: str, level=ExceptionLevel.INFO):
        message = message if level == ExceptionLevel.INFO else f"Error: {message}"
        super().__init__(message)
