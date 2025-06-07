from datetime import datetime
from database import ensure_database
from models import metadata
import cli

ensure_database(metadata)

print("                       🚀 TODO App 🚀")
print(f"             Version: 1.0.0    {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")
print("                       WELCOME BACK!", end="\n\n\n\n")

cli.loop()
