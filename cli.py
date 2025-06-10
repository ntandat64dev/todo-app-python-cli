import argparse
import shlex
import sys

from services import *

# [TODO] - Fix: Type something right after start app, before the prompt to appear.


global_parser = argparse.ArgumentParser(exit_on_error=False)

subparsers = global_parser.add_subparsers(
    title="subcommands",
    dest="command",
    required=True,
)


login_parser = subparsers.add_parser("login", exit_on_error=False)
login_parser.set_defaults(func=login)
login_parser.add_argument("username_and_password")

signup_parser = subparsers.add_parser("signup", exit_on_error=False)
signup_parser.set_defaults(func=sign_up)
signup_parser.add_argument("username_and_password")

deleteuser_parser = subparsers.add_parser("deleteuser", exit_on_error=False)
deleteuser_parser.set_defaults(func=delete_user)
deleteuser_parser.add_argument("id_or_username")

todo_parser = subparsers.add_parser("todo", exit_on_error=False)
todo_parser.set_defaults(func=todo)

todo_parser.add_argument("-a", "--add")
todo_parser.add_argument("-l", "--list", action="store_true")

edit_parser = todo_parser.add_subparsers(dest="edit", action="store_true")
# [TODO]
id_parser = edit_parser.add_parser("id")
edit_parser.add_parser("title")
edit_parser.add_parser("description")


prompt = "🖕 "


def ensure_prompt():
    global prompt
    prompt = "🖕 " if current_user is None else f"🖕 {current_user.username}: "


def loop():
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:
                continue
            if user_input in ["exit", "quit"]:
                break
            args = global_parser.parse_args(shlex.split(user_input))
            args.func(args)
        except:
            value = sys.exc_info()[1]
            print(value)
        else:
            ensure_prompt()
        continue
