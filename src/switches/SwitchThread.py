import threading

from SwitchesClient import SwitchesClient


class SwitchThread(threading.Thread):
    def __init__(self, q):
        self.q = q
        self.switchClient = SwitchesClient()
        super(SwitchThread, self).__init__()

    def connect(self, device_id):
        self.__device_id = device_id
        self.switchClient.connect(device_id)

    def configure(self, readings):
        self.__readings = readings

    def disconnect(self):
        self.switchClient._disconnect(self.device_id)

    def run(self):
        try:
            while True:
                self.switchClient.read_device(
                    self.__readings[0],
                    self.__readings[1],
                    self.__readings[2])

        finally:
            self.disconnect()
