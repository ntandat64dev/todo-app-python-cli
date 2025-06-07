from sqlalchemy import MetaData, create_engine

USERNAME = "postgres"
PASSWORD = "postgres"
HOST = "localhost"
PORT = 5432
DB_NAME = "todo-db"

engine = create_engine(f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}")


def ensure_database(metadata: MetaData):
    # metadata.drop_all(engine, checkfirst=True)
    metadata.create_all(engine, checkfirst=True)
