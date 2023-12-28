import threading
import time
from pynput import keyboard

class KeyListener:
    def __init__(self):
        """
        Initializes the object.

        Args:
            self: The object instance.

        Returns:
            None
        """
        self.keys = []
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener_thread = threading.Thread(target=self.listener.run)

    def on_press(self, key):
        """
        Adds the pressed key to the list of keys if it is a character key.

        Parameters:
            key (Key): The key that was pressed.

        Returns:
            None
        """
        try:
            if key == keyboard.Key.space:
                self.keys.append(' ')
            else:
                self.keys.append(key.char)
            # Space between keys to improve readability
            if len(self.keys) > 70:
                self.keys.append('\n')
        except AttributeError:
            pass

    def start_listener(self):
        """
        Starts the listener thread.

        This function starts the listener thread by calling the `start` method on the `listener_thread` object.

        Parameters:
            None

        Returns:
            None
        """
        self.listener_thread.start()

    def stop_listener(self):
        """
        Stop the listener and join the listener thread.

        This function stops the listener and waits for the listener thread to finish execution.

        Parameters:
            None

        Returns:
            None
        """
        self.listener.stop()
        self.listener_thread.join()

    def read_keys(self, timeout=60):
        """
        Reads the keys from the listener for a specified duration.

        Args:
            timeout (float): The duration in seconds to wait for keys.
        
        Returns:
            str: A string containing all the keys read from the listener.
        """
        self.start_listener()

        time.sleep(timeout)

        self.stop_listener()

        return ''.join(self.keys)