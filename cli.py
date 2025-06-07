from enum import Enum

import services
from schema import User

# [TODO] - Fix: Type something right after start app, before the prompt to appear.


class Commands(Enum):
    EXIT = "exit"
    LOGIN = "login"
    SIGNUP = "signup"
    DELETE_USER = "deleteuser"
    TODO = "todo"

    @classmethod
    def of(cls, value):
        try:
            return cls(value)
        except:
            return None


current_user: User | None = None
prompt = "🖕 "


def update_prompt():
    global prompt
    prompt = "🖕 " if current_user is None else f"🖕 {current_user.username}: "


def loop():
    global current_user

    while True:
        user_command = input(prompt)
        tokens = user_command.split()  # [TODO] - Split with quotes ""
        if not tokens:
            continue

        cmd, *args = tokens

        cmd = Commands.of(cmd)

        if not cmd:
            print("Invalid command")

        if cmd == Commands.EXIT:
            break

        if cmd == Commands.LOGIN:
            if current_user:
                print("You already logged in!")
                continue

            if not args or len(args) > 1:
                print("Specify username and password (username:password)")
                continue

            try:
                current_user = services.login(args[0])
            except Exception as e:
                print(e)
                continue

            update_prompt()
            continue

        elif cmd == Commands.SIGNUP:
            if not args or len(args) > 1:
                print("Specify username and password (username:password)")
                continue

            try:
                new_user = services.sign_up(args[0])
                print(f"Added new user {new_user.username}!")
            except Exception as e:
                print(e)
                continue

            continue

        elif cmd == Commands.DELETE_USER:
            if not args or len(args) > 1:
                print("Specify username and password (username:password)")
                continue

            try:
                deleted_user = services.delete_user(args[0])
                print(f"Deleted {deleted_user.username} successfully!")
            except Exception as e:
                print(e)

            continue

        # WIP
        elif cmd == Commands.TODO:
            if not current_user:
                print("Please login first!")
                continue

            if len(args) < 1 or len(args) > 2:
                print("Invalid arguments")
                continue

            try:
                services.todo(*args, current_user)
            except Exception as e:
                print(e)

            continue
