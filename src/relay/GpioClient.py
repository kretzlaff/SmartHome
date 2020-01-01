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

        self.allUp()
        sleep(5)

        for i in OutputPins:
            GPIO.output(i, GPIO.HIGH)

    def allUp(self):
        GPIO.output(37, GPIO.LOW)
        GPIO.output(36, GPIO.LOW)
        GPIO.output(33, GPIO.LOW)
        GPIO.output(18, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)

    def allDown(self):
        GPIO.output(40, GPIO.LOW)
        GPIO.output(38, GPIO.LOW)
        GPIO.output(35, GPIO.LOW)
        GPIO.output(22, GPIO.LOW)
        GPIO.output(16, GPIO.LOW)


GpioClient()
