# Import GPIO Module
import RPi.GPIO as GPIO


class GpioClient:

    def __init__(self):
        # Configures how we are describing our pin numbering
        GPIO.setmode(GPIO.BOARD)
        # Disable Warnings
        GPIO.setwarnings(False)

        # Set the GPIO pins that are required
        self.__outputPins = [7, 11, 12, 13, 15, 16,
                             18, 22, 31, 32, 33, 35, 36, 37, 38, 40]

        # Set the GPIO pins to outputs and set them to off
        for i in self.__outputPins:
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, GPIO.HIGH)

    # Ensure all values are set to off, in case of a crash
    def __del__(self):
        for i in self.__outputPins:
            GPIO.output(i, GPIO.HIGH)

    def allBlindsUpStart(self):
        self.blind1UpStart()
        self.blind2UpStart()
        self.blind3UpStart()
        self.blind4UpStart()
        self.blind5UpStart()

    def allBlindsDownStart(self):
        self.blind1DownStart()
        self.blind2DownStart()
        self.blind3DownStart()
        self.blind4DownStart()
        self.blind5DownStart()

    def allBlindsUpStop(self):
        self.blind1UpStop()
        self.blind2UpStop()
        self.blind3UpStop()
        self.blind4UpStop()
        self.blind5UpStop()

    def allBlindsDownStop(self):
        self.blind1DownStop()
        self.blind2DownStop()
        self.blind3DownStop()
        self.blind4DownStop()
        self.blind5DownStop()

    def blind1UpStart(self):
        self.blind1DownStop()
        GPIO.output(37, GPIO.LOW)

    def blind1UpStop(self):
        GPIO.output(37, GPIO.HIGH)

    def blind2UpStart(self):
        self.blind2DownStop()
        GPIO.output(36, GPIO.LOW)

    def blind2UpStop(self):
        GPIO.output(36, GPIO.HIGH)

    def blind3UpStart(self):
        self.blind3DownStop()
        GPIO.output(33, GPIO.LOW)

    def blind3UpStop(self):
        GPIO.output(33, GPIO.HIGH)

    def blind4UpStart(self):
        self.blind4DownStop()
        GPIO.output(18, GPIO.LOW)

    def blind4UpStop(self):
        GPIO.output(18, GPIO.HIGH)

    def blind5UpStart(self):
        self.blind5DownStop()
        GPIO.output(13, GPIO.LOW)

    def blind5UpStop(self):
        GPIO.output(13, GPIO.HIGH)

    def blind1DownStart(self):
        self.blind1UpStop()
        GPIO.output(40, GPIO.LOW)

    def blind1DownStop(self):
        GPIO.output(40, GPIO.HIGH)

    def blind2DownStart(self):
        self.blind2UpStop()
        GPIO.output(38, GPIO.LOW)

    def blind2DownStop(self):
        GPIO.output(38, GPIO.HIGH)

    def blind3DownStart(self):
        self.blind3UpStop()
        GPIO.output(35, GPIO.LOW)

    def blind3DownStop(self):
        GPIO.output(35, GPIO.HIGH)

    def blind4DownStart(self):
        self.blind4UpStop()
        GPIO.output(22, GPIO.LOW)

    def blind4DownStop(self):
        GPIO.output(22, GPIO.HIGH)

    def blind5DownStart(self):
        self.blind5UpStop()
        GPIO.output(16, GPIO.LOW)

    def blind5DownStop(self):
        GPIO.output(16, GPIO.HIGH)

    def block(self):
        GPIO.output(12, GPIO.LOW)

    def unblock(self):
        GPIO.output(12, GPIO.HIGH)
