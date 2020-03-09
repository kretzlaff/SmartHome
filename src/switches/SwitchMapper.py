#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from switches import SwitchesClient as c

import datetime


class SwitchMapper(object):
    __device1_id = "01E19747"
    __device2_id = "01E196D1"

    def __init__(self):

        self.__d1 = c.SwitchesClient()
        self.__d2 = c.SwitchesClient()

        self.living_room_3 = self.__d1._A0.pipe()
        self.living_room_1 = self.__d1._A1.pipe()
        self.living_room_2 = self.__d1._A2.pipe()
        self.living_room_4 = self.__d1._A3.pipe()
        self.bedroom_1 = self.__d1._A4.pipe()
        self.bedroom_2 = self.__d1._A5.pipe()
        self.bedroom_3 = self.__d1._A6.pipe()
        # self.__d1._A7.subscribe(lambda value: print("D1A7 pressed"))

        self.bedroom_4 = self.__d1._B0.pipe()
        self.kitchen_3 = self.__d1._B1.pipe()
        self.kitchen_2 = self.__d1._B2.pipe()
        self.kitchen_4 = self.__d1._B3.pipe()
        self.kitchen_1 = self.__d1._B4.pipe()
        # self.__d1._B5.subscribe(lambda value: print("D1B5 pressed"))
        # self.__d1._B6.subscribe(lambda value: print("D1B6 pressed"))
        # self.__d1._B7.subscribe(lambda value: print("D1B7 pressed"))

        self.kitchen_8 = self.__d1._C0.pipe()
        self.kitchen_7 = self.__d1._C1.pipe()
        self.kitchen_5 = self.__d1._C2.pipe()
        self.kitchen_6 = self.__d1._C3.pipe()
        # self.__d1._C4.subscribe(lambda value: print("D1C4 pressed"))
        # self.__d1._C5.subscribe(lambda value: print("D1C5 pressed"))
        # self.__d1._C6.subscribe(lambda value: print("D1C6 pressed"))
        # self.__d1._C7.subscribe(lambda value: print("D1C7 pressed"))

        self.entrance_3 = self.__d2._A0.pipe()
        self.entrance_1 = self.__d2._A1.pipe()
        self.entrance_2 = self.__d2._A2.pipe()
        # self.__d2._A3.subscribe(lambda value: print("D2A3 pressed"))
        self.doorBell = self.__d2._A4.pipe()
        # self.__d2._A5.subscribe(lambda value: print("D2A5 pressed"))
        # self.__d2._A6.subscribe(lambda value: print("D2A6 pressed"))
        # self.__d2._A7.subscribe(lambda value: print("D2A7 pressed"))

        # self.__d2._B0.subscribe(lambda value: print("D2B0 pressed"))
        self.bathroom_1 = self.__d2._B1.pipe()
        self.bathroom_2 = self.__d2._B2.pipe()
        self.bathroom_3 = self.__d2._B3.pipe()
        # self.__d2._B4.subscribe(lambda value: print("D2B4 pressed"))
        # self.__d2._B5.subscribe(lambda value: print("D2B5 pressed"))
        # self.__d2._B6.subscribe(lambda value: print("D2B6 pressed"))
        # self.__d2._B7.subscribe(lambda value: print("D2B7 pressed"))

        self.bedroom_7 = self.__d2._C0.pipe()
        self.bedroom_6 = self.__d2._C1.pipe()
        self.bedroom_8 = self.__d2._C2.pipe()
        self.bedroom_5 = self.__d2._C3.pipe()
        # self.__d2._C4.subscribe(lambda value: print("D2C4 pressed"))
        # self.__d2._C5.subscribe(lambda value: print("D2C5 pressed"))
        # self.__d2._C6.subscribe(lambda value: print("D2C6 pressed"))
        # self.__d2._C7.subscribe(lambda value: print("D2C7 pressed"))

    def readDevices(self):
        try:
            self.__d1.connect("01E19747")
            self.__d2.connect("01E196D1")

            while True:
                self.__d2.read_device([4], [], [])  # Doorbell
                self.__d1.read_device([0, 1, 2, 3, 4, 5, 6],
                                      [0, 1, 2, 3, 4],
                                      [0, 1, 2, 3])
                self.__d2.read_device([4], [], [])  # Doorbell
                self.__d2.read_device([0, 1, 2, 4],
                                      [1, 2, 3],
                                      [0, 1, 2, 3])
        finally:
            self.__d1._disconnect()
            self.__d2._disconnect()
