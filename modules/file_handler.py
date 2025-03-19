import re
import os
import platform
from datetime import datetime



# class File_Handler():
#     def __init__(self):
#         pass

#     def _format_path_for_user(self, output_path):
#         """
#         Convert internal normalized paths (with /) to user-friendly paths (with \\ for Windows).

#         Args:
#             output_path (str): The normalized path.

#         Returns:
#             str: The path formatted for the user's OS.
#         """
#         if platform.system().lower() == "windows":
#             return output_path.replace("/", "\\")
#         return output_path

#     def normalize_path(self, input_path):
#         """
#         Normalize the input path based on the operating system.

#         Args:
#             input_path (str): The user-provided path.

#         Returns:
#             str: The normalized path with forward slashes for internal processing.
#         """
#         if platform.system().lower() == "windows":
#             return input_path.replace("\\", "/")  # Normalize to forward slashes
#         return input_path

#     def parse_command(self, input_text):
#         """
#         Parse the input text for a command using the <:pattern and :>optional_end pattern.
#         Returns:
#             Tuple of:
#             - data_before (str): Text before the command, including '<:' and the single character after it.
#             - command (str): The command without markers or surrounding spaces.
#             - data_after (str): Text after the command, including ':>' and optional spaces before.
#         """
#         logging.info(f"Parsing command: {input_text}")
        
#         # Adjusted regex pattern to include single character after <: in data_before
#         full_pattern = r"(.*?<:.\s*)(.*?)(\s*:>.*|$)"
        
#         # Search for the pattern in the input text
#         match = re.match(full_pattern, input_text)

#         if match:
#             # Extract the components
#             data_before = match.group(1)  # Text before the command, including '<:' and trailing spaces
#             command = match.group(2).strip()  # The command itself, stripped of surrounding spaces
#             data_after = match.group(3)  # Text after the command, including ':>' and leading spaces
#             return data_before, command, data_after

#         # If no match, return None for all parts
#         return None, None, None

#     def autocomplete_path(self, current_path):
#         """
#         Autocomplete the given absolute file or directory path.

#         Args:
#             current_path (str): The current absolute file path input.

#         Returns:
#             str: The autocompleted path or the original path if no match is found.
#         """
#         # Normalize the path for consistent handling
#         logging.info(f"Autocomplete current path: {current_path}")
#         current_path = self.normalize_path(current_path)
#         current_path = os.path.expanduser(current_path)  # Handle ~ for user home directory
#         directory, partial = os.path.split(current_path)
#         logging.info(f"Autocomplete split path: {current_path}, directory: {directory}, partial: {partial}")

#         # If the directory doesn't exist yet, return the current input
#         if not os.path.exists(directory):
#             logging.error(f"Directory does not exist: {directory}")
#             return self._format_path_for_user(current_path)

#         try:
#             # Get matching files and folders in the directory
#             matches = [
#                 f for f in os.listdir(directory)
#                 if f.startswith(partial)
#             ]
#         except FileNotFoundError:
#             logging.error(f"Error accessing directory: {directory}")
#             return self._format_path_for_user(current_path)

#         if matches:
#             logging.info(f"Autocomplete matches: {matches}")

#             # If there's only one match, autocomplete it
#             if len(matches) == 1:
#                 completed_path = os.path.join(directory, matches[0])
#                 return self._format_path_for_user(completed_path + ("/" if os.path.isdir(completed_path) else ""))

#             # If multiple matches, return the longest common prefix
#             common_prefix = os.path.commonprefix(matches)
#             completed_path = os.path.join(directory, common_prefix)

#             # If the common prefix leads to a valid directory or file, autocomplete it
#             if os.path.exists(completed_path):
#                 return self._format_path_for_user(completed_path + ("/" if os.path.isdir(completed_path) else ""))

#         return self._format_path_for_user(current_path)




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
                with open(f"projects/{files[choice - 1]}", 'r') as f:
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