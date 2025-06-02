from sqlalchemy import create_engine

USERNAME = "postgres"
PASSWORD = "postgres"
HOST = "localhost"
PORT = 5432
DB_NAME = "todo-db"

engine = create_engine(f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}")
