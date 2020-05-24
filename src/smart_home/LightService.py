from mqtt import MqttClient, MqttMessageBuilder
from smart_home import RoomGroup
from datetime import datetime
from collections import namedtuple

import threading
import time
from rx import Observable
from rx import operators as ops
from rx.scheduler import NewThreadScheduler

SwitchState = namedtuple('SwitchState', 'pressed, datetime')
DimmState = namedtuple('DimmState', 'value, increase')
TempState = namedtuple('TempState', 'value, increase')


class LightService(object):
    def __init__(self):
        self.__mqttClient = MqttClient.MqttClient()
        self.__lightOn = {}
        self.__lightTemp = {}
        self.__buttonStateHistory = {}
        self.__dimmState = {}
        self.__tempState = {}
        self.__roomRoutineActive = {}
        self.__newThreadScheduler = NewThreadScheduler()

    def addSwitch(self, observable: Observable, roomGroup: RoomGroup):
        self.__dimmState[roomGroup] = DimmState(200, True)
        self.__tempState[roomGroup] = TempState(500, False)
        self.__roomRoutineActive[roomGroup] = False
        self.__lightOn[roomGroup] = False
        observable.subscribe(
            lambda active: self.__pressedHandler(roomGroup) if active else self.__releasedHandler(roomGroup))

    def addTempSwitch(self, observable: Observable, roomGroup: RoomGroup):
        observable.pipe(ops.debounce(0.5)).subscribe(
            lambda active: self.__changeTemperature(roomGroup))

    def __pressedHandler(self, roomGroup: RoomGroup):
        # Key does not yet exist
        if roomGroup not in self.__buttonStateHistory:
            self.__buttonStateHistory[roomGroup] = []

        # List is not empty and Last entry is true
        if self.__buttonStateHistory[roomGroup]:
            if True in self.__buttonStateHistory[roomGroup][-1]:
                return

        # Set Value
        self.__buttonStateHistory[roomGroup].append(
            SwitchState(True, datetime.now()))

        # Start new routine
        self.__startNewLightRoutine(roomGroup)

    def __releasedHandler(self, roomGroup: RoomGroup):
        # Key does not yet exist
        if roomGroup not in self.__buttonStateHistory:
            return

        # List is empty
        if not self.__buttonStateHistory[roomGroup]:
            return

        # Set value
        self.__buttonStateHistory[roomGroup].append(
            SwitchState(False, datetime.now()))

    def __startNewLightRoutine(self, roomGroup: RoomGroup):
        # Ignore if running
        if self.__roomRoutineActive[roomGroup]:
            return

        self.__roomRoutineActive[roomGroup] = True
        t = threading.Thread(target=self.__startRoomRoutine,
                             kwargs={'roomGroup': roomGroup})
        t.start()

    def __startRoomRoutine(self, roomGroup: RoomGroup):
        dimmed = False
        lightOn = True
        if not self.__lightOn[roomGroup]:
            lightOn = False
            self.__turnOnRoom(roomGroup)

        buttonPressed = datetime.now()

        while True:
            now = datetime.now()

            # Newest element in history
            newest = self.__buttonStateHistory[roomGroup][-1]

            # Button is not hold, light was on, turn off room
            if lightOn and not newest.pressed and not dimmed:
                self.__turnOffRoom(roomGroup)

            # Button is hold
            timeSincePressed = (now - buttonPressed).total_seconds()
            if newest.pressed and timeSincePressed > 2:
                self.__dimmRoom(roomGroup)
                time.sleep(0.4)
                dimmed = True

            # No pressed Signal for 2 seconds (reset routine)
            if not newest.pressed:
                break

        # Allow Start of new routine
        self.__buttonStateHistory[roomGroup] = []
        self.__roomRoutineActive[roomGroup] = False

    def __dimmRoom(self, roomGroup: RoomGroup):
        if self.__dimmState[roomGroup].increase:
            nextNumber = min([self.__dimmState[roomGroup].value + 20, 255])
            self.__dimmState[roomGroup] = DimmState(
                nextNumber, not nextNumber == 255)
        else:
            nextNumber = max([self.__dimmState[roomGroup].value - 20, 10])
            self.__dimmState[roomGroup] = DimmState(
                nextNumber, nextNumber == 10)

        self.__mqttClient.publish(
            self.__getGroupFriendlyName(
                roomGroup),
            MqttMessageBuilder.getChangeBrightnessPayload(self.__dimmState[roomGroup].value))

    def __tempCycle(self, roomGroup: RoomGroup):
        if self.__tempState[roomGroup].increase:
            nextNumber = min([self.__tempState[roomGroup].value + 350, 800])
            self.__tempState[roomGroup] = TempState(
                nextNumber, not nextNumber == 800)
        else:
            nextNumber = max([self.__tempState[roomGroup].value - 350, 100])
            self.__tempState[roomGroup] = TempState(
                nextNumber, nextNumber == 100)

        self.__mqttClient.publish(
            self.__getGroupFriendlyName(
                roomGroup),
            MqttMessageBuilder.getChangeTempPayload(self.__tempState[roomGroup].value))

    def __toggleRoom(self, roomGroup: RoomGroup):
        if self.__lightOn[roomGroup]:
            self.__turnOffRoom(roomGroup)
        else:
            self.__turnOnRoom(roomGroup)

    def __turnOffRoom(self, roomGroup: RoomGroup):
        self.__mqttClient.publish(
            self.__getGroupFriendlyName(
                roomGroup),
            MqttMessageBuilder.getTurnOffPayload())
        self.__lightOn[roomGroup] = False

    def __turnOnRoom(self, roomGroup: RoomGroup):
        self.__mqttClient.publish(
            self.__getGroupFriendlyName(
                roomGroup),
            MqttMessageBuilder.getTurnOnPayload())
        self.__lightOn[roomGroup] = True

    def __changeTemperature(self, roomGroup: RoomGroup):
        newLightTemp = 800
        if self.__lightTemp[roomGroup] == 800:
            newLightTemp = 100

        self.__mqttClient.publish(
            self.__getGroupFriendlyName(
                roomGroup),
            MqttMessageBuilder.getChangeTempPayload(newLightTemp))
        self.__lightOn[roomGroup] = True
        self.__lightTemp[roomGroup] = newLightTemp

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
