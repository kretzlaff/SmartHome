from switches import SwitchMapper
from mqtt import MqttClient, MqttMessageBuilder
from smart_home import RoomGroup
import rx
from rx import Observable, operators as ops


class LightService(object):
    def __init__(self):
        self.__mqttClient = MqttClient.MqttClient()
        self.__roomStatus = {}

    def addSwitch(self, observable: Observable, roomGroup: RoomGroup):
        observable.pipe(ops.debounce(1)).subscribe(
            lambda _: self.__toggleRoom(roomGroup))


    def __toggleRoom(self, roomGroup: RoomGroup):
        if roomGroup in self.__roomStatus:
            if self.__roomStatus[roomGroup]:
                self.__turnOffRoom(roomGroup)
                self.__roomStatus[roomGroup] = False
            else:
                self.__turnOnRoom(roomGroup)
                self.__roomStatus[roomGroup] = True
        else:
            self.__turnOnRoom(roomGroup)
            self.__roomStatus[roomGroup] = True

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
