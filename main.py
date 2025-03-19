from modules import adapter, file_handler as fh
import sys
import environ

env = environ.Env()
environ.Env.read_env()
ad = adapter.Adapter(env)
max_tokens = 2000
is_local = True if env("LLM_TYPE") == "local" else False

if is_local:
    from modules import active_mem 
    max_tokens = int(env("OLLAMA_TOKENS"))
    if max_tokens < 1000:
        raise ValueError("The number of tokens must be greater than 1000")
    max_tokens = max_tokens-500
    am = active_mem.TokenLimitedString(max_tokens)

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
        if is_local:
            print(f"[current active mem length: {len(am.value)}]\n")
        chat = input(">>> ").strip()
        if chat.startswith("/"):
            parse_command(chat)
        else:
            if is_local:
                history = am.value
            else:
                history = chat_history
            result = ad.chat(chat, history)
            print(result)
            chat_history += f"user: {chat}\nsystem: {result}\n"
            if is_local:
                am.add_data(chat_history)
    
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"[Error starting: {e}")
        sys.exit(1)