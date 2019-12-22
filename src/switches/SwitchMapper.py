#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from switches import SwitchesClient as c
import rx
from rx import Observable
from time import sleep


class SwitchMapper(object):
    __device1_id = "01E19747"
    __device2_id = "01E196D1"

    def __init__(self):

        d1 = c.SwitchesClient()
        d2 = c.SwitchesClient()

        self.living_room_3 = d1._A0.pipe()
        self.living_room_1 = d1._A1.pipe()
        self.living_room_2 = d1._A2.pipe()
        self.living_room_4 = d1._A3.pipe()
        self.bedroom_1 = d1._A4.pipe()
        self.bedroom_2 = d1._A5.pipe()
        self.bedroom_3 = d1._A6.pipe()
        # d1._A7.subscribe(lambda value: print("D1A7 pressed"))

        self.bedroom_4 = d1._B0.pipe()
        self.kitchen_3 = d1._B1.pipe()
        self.kitchen_2 = d1._B2.pipe()
        self.kitchen_4 = d1._B3.pipe()
        self.kitchen_1 = d1._B4.pipe()
        # d1._B5.subscribe(lambda value: print("D1B5 pressed"))
        # d1._B6.subscribe(lambda value: print("D1B6 pressed"))
        # d1._B7.subscribe(lambda value: print("D1B7 pressed"))

        self.kitchen_8 = d1._C0.pipe()
        self.kitchen_7 = d1._C1.pipe()
        self.kitchen_5 = d1._C2.pipe()
        self.kitchen_6 = d1._C3.pipe()
        # d1._C4.subscribe(lambda value: print("D1C4 pressed"))
        # d1._C5.subscribe(lambda value: print("D1C5 pressed"))
        # d1._C6.subscribe(lambda value: print("D1C6 pressed"))
        # d1._C7.subscribe(lambda value: print("D1C7 pressed"))

        self.entrance_3 = d2._A0.pipe()
        self.entrance_1 = d2._A1.pipe()
        self.entrance_2 = d2._A2.pipe()
        # d2._A3.subscribe(lambda value: print("D2A3 pressed"))
        # d2._A4.subscribe(lambda value: print("D2A4 pressed"))
        # d2._A5.subscribe(lambda value: print("D2A5 pressed"))
        # d2._A6.subscribe(lambda value: print("D2A6 pressed"))
        # d2._A7.subscribe(lambda value: print("D2A7 pressed"))

        # d2._B0.subscribe(lambda value: print("D2B0 pressed"))
        self.bathroom_1 = d2._B1.pipe()
        self.bathroom_2 = d2._B2.pipe()
        self.bathroom_3 = d2._B3.pipe()
        # d2._B4.subscribe(lambda value: print("D2B4 pressed"))
        # d2._B5.subscribe(lambda value: print("D2B5 pressed"))
        # d2._B6.subscribe(lambda value: print("D2B6 pressed"))
        # d2._B7.subscribe(lambda value: print("D2B7 pressed"))

        self.bedroom_7 = d2._C0.pipe()
        self.bedroom_6 = d2._C1.pipe()
        self.bedroom_8 = d2._C2.pipe()
        self.bedroom_5 = d2._C3.pipe()
        # d2._C4.subscribe(lambda value: print("D2C4 pressed"))
        # d2._C5.subscribe(lambda value: print("D2C5 pressed"))
        # d2._C6.subscribe(lambda value: print("D2C6 pressed"))
        # d2._C7.subscribe(lambda value: print("D2C7 pressed"))

        d1.connect("01E19747")
        d2.connect("01E196D1")

        try:
            while True:
                d1.read_device()
                d2.read_device()
                sleep(0.05)
        finally:
            d1._disconnect()
            d2._disconnect()
