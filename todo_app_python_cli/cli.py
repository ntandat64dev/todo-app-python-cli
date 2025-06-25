import argparse
import shlex

from services import current_user, process_command

# [TODO] - Fix: Type something right after start app, before the prompt to appear.

# Set up parsers
parser = argparse.ArgumentParser(prog="")
subparsers = parser.add_subparsers(
    dest="command",
    required=True,
    help="Available commands",
)

# user parser
user_parser = subparsers.add_parser("user")
user_subparser = user_parser.add_subparsers(dest="user_action")
# user add
add_user_parser = user_subparser.add_parser("add")
add_user_parser.add_argument("credentials")
# user login
login_user_parser = user_subparser.add_parser("login")
login_user_parser.add_argument("credentials")
# user del
del_user_parser = user_subparser.add_parser("del")
del_user_parser.add_argument("username")

# todo parser
todo_parser = subparsers.add_parser("todo")
todo_subparser = todo_parser.add_subparsers(dest="todo_action")
# todo list
list_todo_parser = todo_subparser.add_parser("list")
list_todo_parser.add_argument("--title", "-t")
list_todo_parser.add_argument("--desc", "-d")
list_todo_parser.add_argument("--date", "-dt")
list_todo_parser.add_argument("--priority", "-p")
list_todo_parser.add_argument("--completed", "-c")
list_todo_parser.add_argument("--created_at", "-cre")
# todo list
add_todo_parser = todo_subparser.add_parser("add")
add_todo_parser.add_argument("--title", "-t")
add_todo_parser.add_argument("--desc", "-d")
add_todo_parser.add_argument("--date", "-dt")
add_todo_parser.add_argument("--priority", "-p")
# todo edit
edit_todo_parser = todo_subparser.add_parser("edit")
edit_todo_parser.add_argument("id")
edit_todo_parser.add_argument("--title", "-t")
edit_todo_parser.add_argument("--desc", "-d")
edit_todo_parser.add_argument("--date", "-dt")
edit_todo_parser.add_argument("--priority", "-p")
edit_todo_parser.add_argument("--completed", "-c")
# todo del
del_todo_parser = todo_subparser.add_parser("del")
del_todo_parser.add_argument("id_or_title")
# todo done
done_todo_parser = todo_subparser.add_parser("done")
done_todo_parser.add_argument("id_or_title")


def loop():
    prompt = "🖕 " if current_user is None else f"🖕 {current_user.username}> "
    while True:
        try:
            line = input(prompt).strip()
            if not line:
                continue
            if line in ("exit", "quit"):
                break
            args = parser.parse_args(shlex.split(line))
            process_command(args)
        except SystemExit:
            # Triggered by `argparse` on error or by -h/--help.
            # Catch to prevent application from closing.
            pass
        except Exception as e:
            # Other errors.
            print(f"An error occured: {e}")
            pass
