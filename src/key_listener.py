import threading
import time
from pynput import keyboard

class KeyListener:
    def __init__(self):
        self.keys = []
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener_thread = threading.Thread(target=self.listener.run)

    def on_press(self, key):
        try:
            self.keys.append(key.char)
        except AttributeError:
            pass

    def start_listener(self):
        self.listener_thread.start()

    def stop_listener(self):
        self.listener.stop()
        self.listener_thread.join()

    def read_keys(self, timeout=0):
        self.start_listener()

        time.sleep(timeout)

        self.stop_listener()
        return ''.join(self.keys)