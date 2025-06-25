from datetime import datetime
from database import ensure_database
from models import metadata
import cli


def show_greet():
    print("\t\t\t   🚀 TODO App 🚀")
    print(f"\t\tVersion: 1.0.0    {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\t\t\t   WELCOME BACK!", end="\n\n\n\n")


if __name__ == "__main__":
    ensure_database(metadata)
    show_greet()
    cli.loop()
