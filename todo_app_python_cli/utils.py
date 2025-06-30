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
def table_print(records: dict[str, Any], columns_mapping: dict[str, str]):
    columns_length = len(columns_mapping)
    console = Console()
    table = Table(*columns_mapping.values(), box=False)
    for record in records:
        cells = [str(record[field]) for field in columns_mapping]
        cells = cells[:columns_length] + [""] * max(0, columns_length - len(cells))
        table.add_row(*cells)
    console.print(table)
