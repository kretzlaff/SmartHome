from switches import SwitchMapper
from smart_home import LightService, RoomGroup, BlindsService, DoorbellService
from smart_home.BlindAction import BlindAction, Blind
import asyncio

# Init Services
mapper = SwitchMapper.SwitchMapper()
lightService = LightService.LightService()
blindsService = BlindsService.BlindsService()
doorbellService = DoorbellService.DoorbellService()

# Doorbell
doorbellService.addSwitch(mapper.doorBell)

# Map Lights and switches
lightService.addSwitch(mapper.living_room_1, RoomGroup.RoomGroup.LIVING_ROOM)
lightService.addSwitch(mapper.living_room_2, RoomGroup.RoomGroup.OFFICE)
lightService.addSwitch(mapper.kitchen_1, RoomGroup.RoomGroup.KITCHEN)
lightService.addSwitch(mapper.kitchen_5, RoomGroup.RoomGroup.KITCHEN)
lightService.addSwitch(mapper.bathroom_1, RoomGroup.RoomGroup.BATHROOM)
lightService.addSwitch(mapper.bedroom_1, RoomGroup.RoomGroup.BEDROOM)
lightService.addSwitch(mapper.bedroom_5, RoomGroup.RoomGroup.BEDROOM)

# Map Blinds and switches
blindsService.addSwitch(mapper.living_room_3,
                        BlindAction.Blind1Down, Blind.Blind1)
blindsService.addSwitch(mapper.living_room_4,
                        BlindAction.Blind1Up, Blind.Blind1)

blindsService.addSwitch(mapper.kitchen_7, BlindAction.Blind2Up, Blind.Blind2)
blindsService.addSwitch(mapper.kitchen_8, BlindAction.Blind2Down, Blind.Blind2)
blindsService.addSwitch(mapper.kitchen_7, BlindAction.Blind3Up, Blind.Blind3)
blindsService.addSwitch(mapper.kitchen_8, BlindAction.Blind3Down, Blind.Blind3)

blindsService.addSwitch(mapper.kitchen_3, BlindAction.Blind4Up, Blind.Blind4)
blindsService.addSwitch(mapper.kitchen_4, BlindAction.Blind4Down, Blind.Blind4)

blindsService.addSwitch(mapper.bedroom_3, BlindAction.AllUp2, Blind.All)
blindsService.addSwitch(mapper.bedroom_4, BlindAction.AllDown2, Blind.All)

blindsService.addSwitch(mapper.bedroom_7, BlindAction.Blind5Up, Blind.Blind5)
blindsService.addSwitch(mapper.bedroom_8, BlindAction.Blind5Down, Blind.Blind5)

blindsService.addSwitch(mapper.entrance_2, BlindAction.AllUp, Blind.All)
blindsService.addSwitch(mapper.entrance_3, BlindAction.AllDown, Blind.All)

# Start reading switch states
# loop = asyncio.get_event_loop()
# loop.create_task(mapper.readDevices())
# loop.run_forever()
# loop.close()
mapper.readDevices()
