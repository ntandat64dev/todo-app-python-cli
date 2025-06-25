from typing import Any
from bcrypt import checkpw, gensalt, hashpw
from rich.console import Console
from rich.table import Table


def get_hash_password(plain_text_password: str) -> str:
    password_bytes = plain_text_password.encode("utf8")
    hashed_password = hashpw(password_bytes, gensalt())
    return hashed_password.decode("utf8")


def check_hashed_password(plain_text_password: str, hashed_password: str) -> bool:
    plain_text_password_bytes = plain_text_password.encode("utf8")
    password_bytes = hashed_password.encode("utf8")
    return checkpw(plain_text_password_bytes, password_bytes)


# Print records as table using `rich`.
def table_print(records: list[tuple[Any, ...]], columns: tuple[str, ...]):
    console = Console()
    table = Table(*columns, box=False)
    for record in records:
        cells = [str(cell) for cell in record]
        cells = cells[: len(columns)] + [""] * max(0, len(columns) - len(cells))
        table.add_row(*cells)
    console.print(table)
