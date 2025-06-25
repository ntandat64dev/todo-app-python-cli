from sqlalchemy import MetaData, create_engine

USERNAME = "postgres"
PASSWORD = "postgres"
HOST = "localhost"
PORT = 2345
DB_NAME = "todo-db"

url = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
engine = create_engine(url)


def ensure_database(metadata: MetaData):
    # metadata.drop_all(engine)
    metadata.create_all(engine)
