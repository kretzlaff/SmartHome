from mqtt import MqttClient, MqttMessageBuilder
from smart_home import RoomGroup
from datetime import datetime
from collections import namedtuple

from rx import Observable

SwitchState = namedtuple('SwitchState', 'pressed, datetime')


class LightService(object):
    def __init__(self):
        self.__mqttClient = MqttClient.MqttClient()
        self.__roomToggleState = {}
        self.__buttonStateHistory = {}

    def addSwitch(self, observable: Observable, roomGroup: RoomGroup):
        observable.subscribe(
            lambda active: self.__pressedHandler(roomGroup) if active else self.__releasedHandler(roomGroup))

    def __pressedHandler(self, roomGroup: RoomGroup):
        # Key does not yet exist
        if roomGroup not in self.__buttonStateHistory:
            self.__buttonStateHistory[roomGroup] = []

        # List is not empty and Last entry is true
        if self.__buttonStateHistory[roomGroup]:
            if True in self.__buttonStateHistory[roomGroup][-1]:
                return

        # Value changed from pressed to released
        self.__buttonStateHistory[roomGroup].append((True, datetime.now()))
        self.__startNewLightRoutine(roomGroup)

    def __releasedHandler(self, roomGroup: RoomGroup):
        # Key does not yet exist
        if roomGroup not in self.__buttonStateHistory:
            return

        # List is empty
        if not self.__buttonStateHistory[roomGroup]:
            return

        # Last entry is false
        if False in self.__buttonStateHistory[roomGroup][-1]:
            return

        # Value changed from pressed to released
        self.__buttonStateHistory[roomGroup].append(
            SwitchState(False, datetime.now()))

    def __startNewLightRoutine(self, roomGroup: RoomGroup):
        # TODO: Logic :D
        return

    # make sure to start in separate thread
    def __startRoomRoutine(self, roomGroup: RoomGroup):
        while True:
            # Switch has been pressed once (Toggle Light)
            # Switch is hold (Dimm)
            # Switch is pressed twice and then hold (TempCycle)
            # Switch is pressed thrice and then hold (ColorCycle)

            # No pressed Signal for 2 seconds (reset routine)
            # Last entry is False
            if not self.__buttonStateHistory[roomGroup][-1].pressed:
                # Time difference > 2 seconds
                if (datetime.now() - self.__buttonStateHistory[roomGroup][-1].datetime).total_seconds() > 2:
                    self.__buttonStateHistory[roomGroup] = []
                    return

    def __toggleRoom(self, roomGroup: RoomGroup):
        if roomGroup in self.__roomToggleState:
            if self.__roomToggleState[roomGroup]:
                self.__turnOffRoom(roomGroup)
                self.__roomToggleState[roomGroup] = False
            else:
                self.__turnOnRoom(roomGroup)
                self.__roomToggleState[roomGroup] = True
        else:
            self.__turnOnRoom(roomGroup)
            self.__roomToggleState[roomGroup] = True

    def __turnOffRoom(self, roomGroup: RoomGroup):
        self.__mqttClient.publish(
            self.__getGroupFriendlyName(
                roomGroup),
            MqttMessageBuilder.getTurnOffPayload())

    def __turnOnRoom(self, roomGroup: RoomGroup):
        self.__mqttClient.publish(
            self.__getGroupFriendlyName(
                roomGroup),
            MqttMessageBuilder.getTurnOnPayload())

    def __getGroupFriendlyName(self, roomGroup: RoomGroup) -> str:
        if roomGroup == RoomGroup.RoomGroup.BATHROOM:
            return "Bathroom"
        if roomGroup == RoomGroup.RoomGroup.BEDROOM:
            return "Bedroom"
        if roomGroup == RoomGroup.RoomGroup.KITCHEN:
            return "Kitchen"
        if roomGroup == RoomGroup.RoomGroup.LIVING_ROOM:
            return "LivingRoom"
        if roomGroup == RoomGroup.RoomGroup.OFFICE:
            return "Office"
