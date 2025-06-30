from sqlalchemy import MetaData, create_engine, exists, insert, literal, select
from models import users_table
from utils import get_hash_password

USERNAME = "postgres"
PASSWORD = "postgres"
HOST = "localhost"
PORT = 2345
DB_NAME = "todo-db"

url = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
engine = create_engine(url)


def create_admin_user():
    with engine.begin() as conn:
        conn.execute(
            insert(users_table).from_select(
                [users_table.c.username, users_table.c.password, users_table.c.role],
                select(
                    literal("admin"),
                    literal(get_hash_password("admin")),
                    literal("ADMIN"),
                ).where(~exists().where(users_table.c.username == "admin")),
            )
        )


def ensure_database(metadata: MetaData):
    metadata.create_all(engine)
    create_admin_user()
