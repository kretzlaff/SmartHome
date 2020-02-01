# Import GPIO Module
import RPi.GPIO as GPIO
# Import sleep Module for timing
from time import sleep


class GpioClient:

    def __init__(self):
        # Configures how we are describing our pin numbering
        GPIO.setmode(GPIO.BOARD)
        # Disable Warnings
        GPIO.setwarnings(False)

        # Set the GPIO pins that are required
        # OutputPins = [15]
        OutputPins = [7, 11, 12, 13, 15, 16,
                      18, 22, 31, 32, 33, 35, 36, 37, 38, 40]

        # Set the GPIO pins to outputs and set them to off
        for i in OutputPins:
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, GPIO.HIGH)
        sleep(10)
        self.allBlindsUp()
        sleep(10)
        # self.blind3Down()
        # sleep(5)
        # self.blind3Up()
        # sleep(0.1)

        for i in OutputPins:
            GPIO.output(i, GPIO.HIGH)

    def allBlindsUp(self):
        self.blind1Up()
        self.blind2Up()
        self.blind3Up()
        self.blind4Up()
        self.blind5Up()

    def allBlindsDown(self):
        self.blind1Down()
        self.blind2Down()
        self.blind3Down()
        self.blind4Down()
        self.blind5Down()

    def blind1Up(self):
        GPIO.output(37, GPIO.LOW)

    def blind2Up(self):
        GPIO.output(36, GPIO.LOW)

    def blind3Up(self):
        GPIO.output(33, GPIO.LOW)

    def blind4Up(self):
        GPIO.output(18, GPIO.LOW)

    def blind5Up(self):
        GPIO.output(13, GPIO.LOW)

    def blind1Down(self):
        GPIO.output(40, GPIO.LOW)

    def blind2Down(self):
        GPIO.output(38, GPIO.LOW)

    def blind3Down(self):
        GPIO.output(35, GPIO.LOW)

    def blind4Down(self):
        GPIO.output(22, GPIO.LOW)

    def blind5Down(self):
        GPIO.output(16, GPIO.LOW)


GpioClient()
