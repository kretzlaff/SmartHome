import threading
from switches.SwitchesClient import SwitchesClient


class SwitchThread(threading.Thread):
    def __init__(self):
        self.switchClient = SwitchesClient()
        super(SwitchThread, self).__init__()

    def connect(self, device_id):
        self.__device_id = device_id
        self.switchClient.connect(device_id)

    def configure(self, a, b, c):
        self.__a = a
        self.__b = b
        self.__c = c

    def disconnect(self):
        self.switchClient._disconnect()

    def run(self):
        try:
            while True:
                self.switchClient.read_device(
                    self.__a,
                    self.__b,
                    self.__c)
        finally:
            self.disconnect()
