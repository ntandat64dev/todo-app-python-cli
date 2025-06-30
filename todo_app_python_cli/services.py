import utils
from database import engine
from exceptions import AppException, ExceptionLevel
from models import Priority, Role, todos_table, users_table
from schema import Todo, User
from sqlalchemy import and_, delete, exists, insert, select, update
from rich.table import Column

current_user: User | None = None
is_admin = False


def process_command(args):
    if args.command == "user":
        if args.user_action == "add":
            sign_up(args)
        elif args.user_action == "login":
            login(args)
        elif args.user_action == "del":
            delete_user(args)
    elif args.command == "todo":
        if args.todo_action == "list":
            list_todo(args)
        elif args.todo_action == "add":
            add_todo(args)
        elif args.todo_action == "edit":
            edit_todo(args)
        elif args.todo_action == "del":
            delete_todo(args)
        elif args.todo_action == "done":
            done_todo(args)
    elif args.command == "logout":
        logout()


def login(args) -> None:
    global current_user
    global is_admin

    if current_user:
        raise AppException("You already logged in.")

    username, password = args.credentials.split(":", 1)
    with engine.begin() as conn:
        result = conn.execute(
            select(users_table).where(users_table.c.username == username)
        )
        if result.rowcount != 1:
            raise AppException(f"User {username} not found.", level=1)

        id, username, hashed_password, role = result.first()
        password_matched = utils.check_hashed_password(
            plain_text_password=password,
            hashed_password=hashed_password,
        )
        if not password_matched:
            raise AppException("Invalid password.", level=ExceptionLevel.ERROR)

        current_user = User(id=id, username=username, role=role)
        is_admin = username == "admin"


def sign_up(args):
    username, password = args.credentials.split(":", 1)
    with engine.begin() as conn:
        result = conn.execute(
            select(
                exists(users_table.c.username).where(
                    users_table.c.username == username
                ),
            )
        )
        user_exist = result.scalar()
        if user_exist:
            raise AppException(f"User '{username}' already exists.", level=1)

        hashed_password = utils.get_hash_password(password)
        conn.execute(
            insert(users_table).values(
                username=username,
                role=Role.USER,
                password=hashed_password,
            )
        )
        print(f"User '{username}' created successfully.")


def delete_user(args) -> None:
    if not is_admin:
        raise AppException("You do not have permission to delete users.", level=1)

    username = args.username
    with engine.begin() as conn:
        result = conn.execute(
            select(users_table).where(users_table.c.username == username)
        )
        if result.rowcount != 1:
            raise AppException(f"User {username} not found.", level=1)
        conn.execute(delete(users_table).where(users_table.c.username == username))
        print(f"User '{username}' and all their TODOs have been deleted.")


def list_todo(args):
    if not current_user:
        raise AppException("You must be logged in to list TODOs.", level=1)

    conditions = []
    if title := getattr(args, "title", None):
        conditions.append(todos_table.c.title == title)
    if desc := getattr(args, "desc", None):
        conditions.append(todos_table.c.description == desc)
    if date := getattr(args, "date", None):
        conditions.append(todos_table.c.due_date == date)
    if priority := getattr(args, "priority", None):
        conditions.append(todos_table.c.priority == priority)
    if completed := getattr(args, "completed", None):
        conditions.append(todos_table.c.completed == completed)
    if created_at := getattr(args, "created_at", None):
        conditions.append(todos_table.c.created_at == created_at)

    with engine.begin() as conn:
        stm = select(todos_table).where(todos_table.c.user_id == current_user.id)
        if conditions:
            stm = stm.where(and_(*conditions))
        result = conn.execute(stm)
        columns_mapping = {
            "id": "ID",
            "title": "TITLE",
            "description": "DESCRIPTION",
            "due_date": "DUE DATE",
            "priority": "PRIORITY",
            "completed": Column("COMPLETED", justify="center"),
            "created_at": "CREATED AT",
        }
        todos = [Todo(**item).model_dump() for item in result.mappings().all()]
        utils.table_print(todos, columns_mapping)


def add_todo(args):
    if not current_user:
        raise AppException("You must be logged in to add TODO.", level=1)

    todo = Todo(
        title=args.title,
        description=args.desc,
        due_date=args.date,
        priority=Priority[args.priority] if args.priority else Priority.MEDIUM,
        user_id=current_user.id,
    )

    values = todo.model_dump(exclude={"id"})

    with engine.begin() as conn:
        result = conn.execute(
            insert(todos_table).values(**values).returning(todos_table.c.id)
        )
        inserted_todo_id = result.scalar()
        print(f"TODO {inserted_todo_id}: '{todo.title}' added successfully.")


def belongs_to_this_user(id_or_title, is_title=False):
    match_todo_stm = (
        todos_table.c.title == id_or_title
        if is_title
        else todos_table.c.id == id_or_title
    )
    with engine.begin() as conn:
        result = conn.execute(
            select(
                exists(
                    select(todos_table).where(
                        and_(
                            todos_table.c.user_id == current_user.id,
                            match_todo_stm,
                        )
                    )
                )
            )
        )
        return result.scalar()


def edit_todo(args):
    if not current_user:
        raise AppException("You must be logged in to update TODOs.", level=1)

    if not belongs_to_this_user(args.id):
        raise AppException(f"TODO {args.id} not found.", level=1)

    values = {}
    if args.title:
        values["title"] = args.title
    if args.desc:
        values["description"] = args.desc
    if args.date:
        values["due_date"] = args.date
    if args.priority:
        values["priority"] = args.priority
    if args.completed:
        values["completed"] = bool(args.completed)

    with engine.begin() as conn:
        conn.execute(
            update(todos_table).where(todos_table.c.id == args.id).values(**values)
        )
        print(f"TODO {args.id} is updated.")


def delete_todo(args):
    if not current_user:
        raise AppException("You must be logged in to delete TODOs.", level=1)

    if not belongs_to_this_user(args.id_or_title, is_title=True):
        raise AppException(f"TODO {args.id_or_title} not found.", level=1)

    try:
        where_stm = todos_table.c.id == int(args.id_or_title)
    except:
        where_stm = todos_table.c.title == str(args.id_or_title)

    with engine.begin() as conn:
        conn.execute(delete(todos_table).where(where_stm))
        print(f"Successfully deleted TODO '{args.id_or_title}'.")


def done_todo(args):
    if not current_user:
        raise AppException("You must be logged in to complete TODO.", level=1)

    if not belongs_to_this_user(args.id_or_title, is_title=True):
        raise AppException(f"TODO {args.id_or_title} not found.", level=1)

    try:
        where_stm = todos_table.c.id == int(args.id_or_title)
    except:
        where_stm = todos_table.c.title == str(args.id_or_title)

    with engine.begin() as conn:
        conn.execute(update(todos_table).values({"completed": True}).where(where_stm))
        print(f"Completed TODO '{args.id_or_title}'.")


def logout():
    global current_user
    if not current_user:
        raise AppException("You must be logged in first.", level=1)

    current_user = None
    print("Good bye!")
