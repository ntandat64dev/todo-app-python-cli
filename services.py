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


def login(arg: str) -> User:
    args = arg.split(":")
    if len(args) < 2 or not args[0] or not args[1]:
        raise InvalidArgument(arg)

    username, password = args

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

        return User(
            id=id,
            username=username,
        )


def sign_up(arg: str) -> User:
    args = arg.split(":")
    if len(args) < 2 or not args[0] or not args[1]:
        raise InvalidArgument(arg)

    username, password = args

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

        return User(id=inserted_row.id, username=inserted_row.username)


def delete_user(arg: str) -> User:
    try:
        id_or_username = int(arg)
    except:
        id_or_username = arg

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

        id, username, *_ = conn.execute(
            delete(users_table)
            .where(users_table.c.id == user_id)
            .returning(users_table)
        ).first()

    return User(id=id, username=username)


def todo(args, current_user: User) -> Todo:
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
        id = result.inserted_primary_key
        if not id:
            raise GeneralError

    todo.id = id
    return todo
