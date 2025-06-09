from re import match

from pydantic import ValidationError
from sqlalchemy import delete, exists, insert, select

import utils
from database import engine
from exceptions import (
    GeneralError,
    InvalidArgument,
    PasswordNotMatch,
    UserAlreadyExist,
    UsernameNotFound,
    UserNotFound,
)
from models import todos_table, users_table
from schema import Todo, User
from validation import process_error

current_user: User | None = None


def login(args) -> None:
    global current_user
    if current_user:
        raise GeneralError(msg="You already logged in!")

    username_and_password = str(args.username_and_password)
    if not (m := match("(.+):(.+)", username_and_password)):
        raise InvalidArgument(username_and_password)
    username, password = m.groups()

    with engine.begin() as conn:
        result = conn.execute(
            select(users_table).where(users_table.c.username == username)
        )

        if result.rowcount != 1:
            raise UsernameNotFound(username)

        id, username, hashed_password = result.first()

        password_matched = utils.check_hashed_password(
            plain_text_password=password, hashed_password=hashed_password
        )

        if not password_matched:
            raise PasswordNotMatch

        current_user = User(
            id=id,
            username=username,
        )


def sign_up(args) -> None:
    username_and_password = str(args.username_and_password)
    if not (m := match("(.+):(.+)", username_and_password)):
        raise InvalidArgument(username_and_password)
    username, password = m.groups()

    with engine.begin() as conn:
        result = conn.execute(
            select(
                exists(users_table.c.username).where(users_table.c.username == username)
            )
        )

        user_exist = result.scalar()
        if user_exist:
            raise UserAlreadyExist(username)

        hashed_password = utils.get_hash_password(password)
        inserted_row = conn.execute(
            insert(users_table)
            .values(username=username, password=hashed_password)
            .returning(users_table)
        ).first()

        if not inserted_row:
            raise GeneralError

        print(f"Added new user {inserted_row.username}!")


def delete_user(args) -> None:
    id_or_username = str(args.id_or_username)
    try:
        id_or_username = int(id_or_username)
    except:
        id_or_username = id_or_username

    with engine.begin() as conn:
        where_column = (
            users_table.c.id
            if isinstance(id_or_username, int)
            else users_table.c.username
        )

        result = conn.execute(select(users_table).where(where_column == id_or_username))
        if result.rowcount != 1:
            raise UserNotFound

        user_id = result.first().id

        _, username, *_ = conn.execute(
            delete(users_table)
            .where(users_table.c.id == user_id)
            .returning(users_table)
        ).first()

    print(f"Deleted {username} successfully!")


def todo(args) -> None:
    if not current_user:
        raise GeneralError(msg="Please login first!")

    if args.add:
        try:
            todo = Todo.model_validate_json(args.add)
        except ValidationError as e:
            raise InvalidArgument(process_error(e, to_json=True))

        todo.user_id = current_user.id

        with engine.begin() as conn:
            result = conn.execute(
                insert(todos_table).values(**todo.model_dump(exclude={"id"}))
            )
            if not result.rowcount:
                raise GeneralError

    elif args.list:
        with engine.begin() as conn:
            result = conn.execute(
                select(todos_table).where(todos_table.c.user_id == users_table.c.id)
            )
            columns = (
                "ID",
                "TITLE",
                "DESCRIPTION",
                "DUE DATE",
                "PRIORITY",
                "COMPLETED",
                "CREATED AT",
            )
            utils.table_print(result, columns)

    # [TODO] - Edit
