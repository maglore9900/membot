from modules import adapter, file_handler as fh
import sys
import environ

env = environ.Env()
environ.Env.read_env()
ad = adapter.Adapter(env)

chat_history = ""

commands = {
    "save": lambda filename=None: fh.save_file(chat_history, filename),
    "load": lambda: fh.select_file(),
    "quit": lambda: sys.exit(0)
}

def parse_command(data, args=None):
    global chat_history
    parts = data.lstrip("/").strip().split(maxsplit=1)
    command = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""
    if command in commands:
        if command == "load":
            chat_history = commands[command]()
        elif command == "save":
            commands[command](args)
        elif command == "quit":
            choice = input("do you want to save your chat history?\nY/N\n")
            if choice.lower() == "y":
                commands["save"]()
            commands[command]()
        elif command == "clear":
            chat_history = ""


while True:
    try:
        chat = input(">>> ").strip()
        if chat.startswith("/"):
            parse_command(chat)
        else:
            result = ad.chat(chat, chat_history)
            print(result)
            chat_history += f"user: {chat}\nsystem: {result}\n"
    
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"[Error starting: {e}")
        sys.exit(1)