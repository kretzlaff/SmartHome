#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from SwitchThread import SwitchThread


class SwitchMapper(object):
    def __init__(self):
        self.__device1_id = "01E19747"
        self.__device2_id = "01E196D1"

        self.__thread1 = SwitchThread()
        self.__thread2 = SwitchThread()

        self.living_room_3 = self.__thread1.switchClient._A0.pipe()
        self.living_room_1 = self.__thread1.switchClient._A1.pipe()
        self.living_room_2 = self.__thread1.switchClient._A2.pipe()
        self.living_room_4 = self.__thread1.switchClient._A3.pipe()
        self.bedroom_1 = self.__thread1.switchClient._A4.pipe()
        self.bedroom_2 = self.__thread1.switchClient._A5.pipe()
        self.bedroom_3 = self.__thread1.switchClient._A6.pipe()
        # self.__thread1.switchClient._A7

        self.bedroom_4 = self.__thread1.switchClient._B0.pipe()
        self.kitchen_3 = self.__thread1.switchClient._B1.pipe()
        self.kitchen_2 = self.__thread1.switchClient._B2.pipe()
        self.kitchen_4 = self.__thread1.switchClient._B3.pipe()
        self.kitchen_1 = self.__thread1.switchClient._B4.pipe()
        # self.__thread1.switchClient._B5
        # self.__thread1.switchClient._B6
        # self.__thread1.switchClient._B7

        self.kitchen_8 = self.__thread1.switchClient._C0.pipe()
        self.kitchen_7 = self.__thread1.switchClient._C1.pipe()
        self.kitchen_5 = self.__thread1.switchClient._C2.pipe()
        self.kitchen_6 = self.__thread1.switchClient._C3.pipe()
        # self.__thread1.switchClient._C4
        # self.__thread1.switchClient._C5
        # self.__thread1.switchClient._C6
        # self.__thread1.switchClient._C7

        self.entrance_3 = self.__thread2.switchClient._A0.pipe()
        self.entrance_1 = self.__thread2.switchClient._A1.pipe()
        self.entrance_2 = self.__thread2.switchClient._A2.pipe()
        # self.__thread2.switchClient._A3
        self.doorBell = self.__thread2.switchClient._A4.pipe()
        # self.__thread2.switchClient._A5
        # self.__thread2.switchClient._A6
        # self.__thread2.switchClient._A7

        # self.__thread2.switchClient._B0
        self.bathroom_1 = self.__thread2.switchClient._B1.pipe()
        self.bathroom_2 = self.__thread2.switchClient._B2.pipe()
        self.bathroom_3 = self.__thread2.switchClient._B3.pipe()
        # self.__thread2.switchClient._B4
        # self.__thread2.switchClient._B5
        # self.__thread2.switchClient._B6
        # self.__thread2.switchClient._B7

        self.bedroom_7 = self.__thread2.switchClient._C0.pipe()
        self.bedroom_6 = self.__thread2.switchClient._C1.pipe()
        self.bedroom_8 = self.__thread2.switchClient._C2.pipe()
        self.bedroom_5 = self.__thread2.switchClient._C3.pipe()
        # self.__thread2.switchClient._C4
        # self.__thread2.switchClient._C5
        # self.__thread2.switchClient._C6
        # self.__thread2.switchClient._C7

    def readDevices(self):
        self.__thread1.configure([0, 1, 2, 3, 4, 5, 6],
                                 [0, 1, 2, 3, 4],
                                 [0, 1, 2, 3])
        self.__thread2.configure([0, 1, 2, 4],
                                 [1, 2, 3],
                                 [0, 1, 2, 3])

        self.__thread1.connect(self.__device1_id)
        self.__thread2.connect(self.__device2_id)

        self.__thread1.run()
        self.__thread2.run()
