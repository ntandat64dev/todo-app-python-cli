from bcrypt import checkpw, gensalt, hashpw


def get_hash_password(plain_text_password: str) -> str:
    password_bytes = plain_text_password.encode("utf8")
    hashed_password = hashpw(password_bytes, gensalt())
    return hashed_password.decode("utf8")


def check_hashed_password(plain_text_password: str, hashed_password: str) -> bool:
    plain_text_password_bytes = plain_text_password.encode("utf8")
    password_bytes = hashed_password.encode("utf8")
    return checkpw(plain_text_password_bytes, password_bytes)
