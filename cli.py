import argparse
import shlex

import services
from schema import User

# [TODO] - Fix: Type something right after start app, before the prompt to appear.


global_parser = argparse.ArgumentParser()

subparsers = global_parser.add_subparsers(
    title="subcommands",
    dest="command",
    required=True,
)

login_parser = subparsers.add_parser("login")
login_parser.add_argument("username_and_password")

signup_parser = subparsers.add_parser("signup")
signup_parser.add_argument("username_and_password")

deleteuser_parser = subparsers.add_parser("deleteuser")
deleteuser_parser.add_argument("id_or_username")

todo_parser = subparsers.add_parser("todo")
todo_parser.add_argument("-a", "--add")

current_user: User | None = None
prompt = "🖕 "


def update_prompt():
    global prompt
    prompt = "🖕 " if current_user is None else f"🖕 {current_user.username}: "


def loop():
    global current_user

    while True:
        user_input = input(prompt)

        if user_input in ["exit", "quit"]:
            break

        args = global_parser.parse_args(shlex.split(user_input))

        if args.command == "login":
            if current_user:
                print("You already logged in!")
                continue
            try:
                current_user = services.login(args.username_and_password)
                update_prompt()
            except Exception as e:
                print(e)

        elif args.command == "signup":
            try:
                new_user = services.sign_up(args.username_and_password)
                print(f"Added new user {new_user.username}!")
            except Exception as e:
                print(e)

        elif args.command == "deleteuser":
            try:
                deleted_user = services.delete_user(args.id_or_username)
                print(f"Deleted {deleted_user.username} successfully!")
            except Exception as e:
                print(e)

        elif args.command == "todo":
            if not current_user:
                print("Please login first!")
                continue
            try:
                services.todo(args, current_user=current_user)
            except Exception as e:
                print(e)

        continue
