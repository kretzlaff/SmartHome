from switches import SwitchMapper
from smart_home import LightService, RoomGroup
import rx
import asyncio

mapper = SwitchMapper.SwitchMapper()
lightService = LightService.LightService()

lightService.addSwitch(mapper.living_room_1, RoomGroup.RoomGroup.LIVING_ROOM)
lightService.addSwitch(mapper.living_room_2, RoomGroup.RoomGroup.OFFICE)
lightService.addSwitch(mapper.kitchen_1, RoomGroup.RoomGroup.KITCHEN)
lightService.addSwitch(mapper.kitchen_5, RoomGroup.RoomGroup.KITCHEN)
lightService.addSwitch(mapper.bathroom_1, RoomGroup.RoomGroup.BATHROOM)
lightService.addSwitch(mapper.bedroom_1, RoomGroup.RoomGroup.BEDROOM)
lightService.addSwitch(mapper.bedroom_5, RoomGroup.RoomGroup.BEDROOM)


loop = asyncio.get_event_loop()
loop.create_task(mapper.readDevices())
loop.run_forever()
loop.close()
