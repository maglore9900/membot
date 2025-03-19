import os
from datetime import datetime

def list_files_in_directory(path='./chat_history'):
    try:
        # List all files and directories in the specified path
        files = os.listdir(path)

        # Filter out directories, keep only files
        files = [f for f in files if os.path.isfile(os.path.join(path, f))]

        return files
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def select_file():
    # Display the files with numbered options
    files = list_files_in_directory()
    for index, file in enumerate(files, start=1):
        print(f"{index}) {file}")

    while True:
        try:
            # Prompt the user to select a file by its number
            choice = int(input("\nEnter the number of the file you want to select: "))

            if 1 <= choice <= len(files):
                with open(f"chat_history/{files[choice - 1]}", 'r') as f:
                    contents = f.read()
                    return contents
            else:
                print("Invalid choice. Please select a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def save_file(data, filename=None):
    now = datetime.now()
    formatted_time = now.strftime("%m%d%y_%H%M")
    if filename:
        name = f"_{filename}"
    else:
        name = ""
    with open(f"chat_history/{formatted_time}{name}.txt", "w") as f:
        f.write(data)

def load_file(filename):
    with open(f"chat_history/{filename}", 'r', encoding="utf8") as f:
        data = f.read()
        return data