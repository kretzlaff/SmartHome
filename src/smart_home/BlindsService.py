import datetime

from rx import Observable
from rx import operators as ops
from rx.scheduler import EventLoopScheduler
from smart_home.BlindAction import BlindAction, Blind
from relay import GpioClient
from threading import Timer


class BlindsService(object):
    def __init__(self):
        self.__gpioClient = GpioClient.GpioClient()
        self.__buttonState = {}
        self.__blindUp = {}
        self.__blindUpTimer = {}
        self.__blockTimer = None
        self.__scheduler = EventLoopScheduler()

    def addSwitch(self,
                  observable: Observable,
                  blindAction: BlindAction,
                  blind: Blind):
        # Initialize states
        self.__buttonState[blindAction] = False
        self.__blindUp[blind] = False

        # Add a handler to the switch state
        observable.pipe(ops.observe_on(self.__scheduler)).subscribe(
            lambda active: self.__pressedHandler(blindAction, blind, active))

    def __pressedHandler(
            self,
            blindAction: BlindAction,
            blind: Blind,
            active: bool):
        # Button State did not change ... skipping
        if self.__buttonState[blindAction] == active:
            return

        # Button State changed ... save it
        self.__buttonState[blindAction] = active

        # Button is pressed
        if active:
            # Unblock blinds
            self.__gpioClient.unblock()

            # Activate relay
            self.__handleRelayActive(blindAction, blind)

        # Button is released
        else:
            # Deactivate relay
            self.__handleRelayInactive(blindAction, blind)

        # Block Wind/Time automation when all blinds are up
        # Dispose existing timer
        if self.__blockTimer is not None:
            self.__blockTimer.cancel()

        # Block the automation after 70 seconds
        self.__blockTimer = Timer(70.0, self.__blockAutomationWhenAllAreUp)
        self.__blockTimer.start()

    def __handleRelayActive(self, blindAction: BlindAction, blind: Blind):
        # Forward the signal to the GPIO Client
        if blindAction == BlindAction.Blind1Up:
            self.__gpioClient.blind1UpStart()
        if blindAction == BlindAction.Blind2Up:
            self.__gpioClient.blind2UpStart()
        if blindAction == BlindAction.Blind3Up:
            self.__gpioClient.blind3UpStart()
        if blindAction == BlindAction.Blind4Up:
            self.__gpioClient.blind4UpStart()
        if blindAction == BlindAction.Blind5Up:
            self.__gpioClient.blind5UpStart()

        if blindAction == BlindAction.Blind1Down:
            self.__gpioClient.blind1DownStart()
        if blindAction == BlindAction.Blind2Down:
            self.__gpioClient.blind2DownStart()
        if blindAction == BlindAction.Blind3Down:
            self.__gpioClient.blind3DownStart()
        if blindAction == BlindAction.Blind4Down:
            self.__gpioClient.blind4DownStart()
        if blindAction == BlindAction.Blind5Down:
            self.__gpioClient.blind5DownStart()

        if (blindAction == BlindAction.AllUp or
                blindAction == BlindAction.AllUp2):
            self.__gpioClient.allBlindsUpStart()
        if (blindAction == BlindAction.AllDown or
                blindAction == BlindAction.AllDown2):
            self.__gpioClient.allBlindsDownStart()

        # Store the timestamp when the up signal was initiated
        # to detect if the blind is all the way up
        if blindAction in (BlindAction.Blind1Up,
                           BlindAction.Blind2Up,
                           BlindAction.Blind3Up,
                           BlindAction.Blind4Up,
                           BlindAction.Blind5Up,
                           BlindAction.AllUp,
                           BlindAction.AllUp2):
            self.__blindUpTimer[blind] = datetime.datetime.now()

    def __handleRelayInactive(self, blindAction: BlindAction, blind: Blind):
        # Forward the signal to the GPIO Client
        if blindAction == BlindAction.Blind1Up:
            self.__gpioClient.blind1UpStop()
        if blindAction == BlindAction.Blind2Up:
            self.__gpioClient.blind2UpStop()
        if blindAction == BlindAction.Blind3Up:
            self.__gpioClient.blind3UpStop()
        if blindAction == BlindAction.Blind4Up:
            self.__gpioClient.blind4UpStop()
        if blindAction == BlindAction.Blind5Up:
            self.__gpioClient.blind5UpStop()

        if blindAction == BlindAction.Blind1Down:
            self.__gpioClient.blind1DownStop()
        if blindAction == BlindAction.Blind2Down:
            self.__gpioClient.blind2DownStop()
        if blindAction == BlindAction.Blind3Down:
            self.__gpioClient.blind3DownStop()
        if blindAction == BlindAction.Blind4Down:
            self.__gpioClient.blind4DownStop()
        if blindAction == BlindAction.Blind5Down:
            self.__gpioClient.blind5DownStop()

        if (blindAction == BlindAction.AllUp or
                blindAction == BlindAction.AllUp2):
            self.__gpioClient.allBlindsUpStop()
        if (blindAction == BlindAction.AllDown or
                blindAction == BlindAction.AllDown2):
            self.__gpioClient.allBlindsDownStop()

        # If the up signal was sent for more than 2 seconds the blind is up
        if blindAction in (BlindAction.Blind1Up,
                           BlindAction.Blind2Up,
                           BlindAction.Blind3Up,
                           BlindAction.Blind4Up,
                           BlindAction.Blind5Up,
                           BlindAction.AllUp,
                           BlindAction.AllUp2):
            blindUp: bool = (datetime.datetime.now() -
                             self.__blindUpTimer[blind]).total_seconds() > 2

            self.__blindUp[blind] = blindUp

            # Change all values in case the group all is triggered
            if (blindAction == BlindAction.AllUp or
                    blindAction == BlindAction.AllUp2):
                for group in Blind:
                    self.__blindUp[group] = blindUp

        # Store that not all blinds are at top
        else:
            self.__blindUp[blind] = False

            # Change all values in case the group all is triggered
            if (blindAction == BlindAction.AllDown or
                    blindAction == BlindAction.AllDown2):
                for group in Blind:
                    self.__blindUp[group] = False

    def __blockAutomationWhenAllAreUp(self):
        # Ensure all 5 blinds are registered
        if Blind.Blind1 not in self.__blindUp:
            return
        if Blind.Blind2 not in self.__blindUp:
            return
        if Blind.Blind3 not in self.__blindUp:
            return
        if Blind.Blind4 not in self.__blindUp:
            return
        if Blind.Blind5 not in self.__blindUp:
            return

        # Ensure all 5 blinds are up
        if not self.__blindUp[Blind.Blind1]:
            return
        if not self.__blindUp[Blind.Blind2]:
            return
        if not self.__blindUp[Blind.Blind3]:
            return
        if not self.__blindUp[Blind.Blind4]:
            return
        if not self.__blindUp[Blind.Blind5]:
            return

        # All blinds are up
        # Block the automation
        self.__gpioClient.block()
