#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from __future__ import print_function
from rx.subject import Subject

from uldaq import (get_daq_device_inventory,
                   DaqDevice,
                   InterfaceType,
                   DigitalDirection)


class SwitchesClient(object):

    def __init__(self):
        # Observers
        self._A0 = Subject()
        self._A1 = Subject()
        self._A2 = Subject()
        self._A3 = Subject()
        self._A4 = Subject()
        self._A5 = Subject()
        self._A6 = Subject()
        self._A7 = Subject()
        self._B0 = Subject()
        self._B1 = Subject()
        self._B2 = Subject()
        self._B3 = Subject()
        self._B4 = Subject()
        self._B5 = Subject()
        self._B6 = Subject()
        self._B7 = Subject()
        self._C0 = Subject()
        self._C1 = Subject()
        self._C2 = Subject()
        self._C3 = Subject()
        self._C4 = Subject()
        self._C5 = Subject()
        self._C6 = Subject()
        self._C7 = Subject()
        self.__lastInputAction = {
            0: {
                0: False,
                1: False,
                2: False,
                3: False,
                4: False,
                5: False,
                6: False,
                7: False,
            },
            1: {
                0: False,
                1: False,
                2: False,
                3: False,
                4: False,
                5: False,
                6: False,
                7: False,
            },
            2: {
                0: False,
                1: False,
                2: False,
                3: False,
                4: False,
                5: False,
                6: False,
                7: False,
            }
        }
        self.__inputActions = {
            0: {
                0: lambda pressed: self._A0.on_next(pressed),
                1: lambda pressed: self._A1.on_next(pressed),
                2: lambda pressed: self._A2.on_next(pressed),
                3: lambda pressed: self._A3.on_next(pressed),
                4: lambda pressed: self._A4.on_next(pressed),
                5: lambda pressed: self._A5.on_next(pressed),
                6: lambda pressed: self._A6.on_next(pressed),
                7: lambda pressed: self._A7.on_next(pressed),
            },
            1: {
                0: lambda pressed: self._B0.on_next(pressed),
                1: lambda pressed: self._B1.on_next(pressed),
                2: lambda pressed: self._B2.on_next(pressed),
                3: lambda pressed: self._B3.on_next(pressed),
                4: lambda pressed: self._B4.on_next(pressed),
                5: lambda pressed: self._B5.on_next(pressed),
                6: lambda pressed: self._B6.on_next(pressed),
                7: lambda pressed: self._B7.on_next(pressed),
            },
            2: {
                0: lambda pressed: self._C0.on_next(pressed),
                1: lambda pressed: self._C1.on_next(pressed),
                2: lambda pressed: self._C2.on_next(pressed),
                3: lambda pressed: self._C3.on_next(pressed),
                4: lambda pressed: self._C4.on_next(pressed),
                5: lambda pressed: self._C5.on_next(pressed),
                6: lambda pressed: self._C6.on_next(pressed),
                7: lambda pressed: self._C7.on_next(pressed),
            }
        }

    def connect(self, device_id):
        self.__daq_device = None

        self.__interface_type = InterfaceType.USB
        self.__descriptor_index = 0
        self.__device_id = device_id

        try:
            # Get descriptors for all of the available DAQ devices.
            self.__devices = get_daq_device_inventory(self.__interface_type)
            self.__number_of_devices = len(self.__devices)
            if self.__number_of_devices == 0:
                raise Exception('Error: No DAQ devices found')

            print('Found', self.__number_of_devices, 'DAQ device(s):')
            for i in range(self.__number_of_devices):
                print('  ', self.__devices[i].product_name,
                      ' (', self.__devices[i].unique_id, ')', sep='')

            # Create the DAQ device object
            # associated with the specified descriptor index.
            self.__device = next(
                f for f in self.__devices if f.unique_id == self.__device_id)

            print('Trying to connect to Device Id: ', self.__device)
            self.__daq_device = DaqDevice(self.__device)

            # Get the DioDevice object and verify that it is valid.
            self.__dio_device = self.__daq_device.get_dio_device()
            if self.__dio_device is None:
                raise Exception(
                    'Error: The DAQ device does not support digital input')

            # Establish a connection to the DAQ device.
            self.__descriptor = self.__daq_device.get_descriptor()
            print('\nConnecting to', self.__descriptor.dev_string)
            self.__daq_device.connect()

            # Get the port types for the device(AUXPORT, FIRSTPORTA, ...)
            self.__dio_info = self.__dio_device.get_info()
            self.__port_types = self.__dio_info.get_port_types()

            self.__port_a = self.__port_types[0]
            self.__port_b = self.__port_types[1]
            self.__port_c = self.__port_types[2]

            # Get the port I/O type and the number of bits for the first port.
            self.__port_info_a = self.__dio_info.get_port_info(self.__port_a)
            self.__port_info_b = self.__dio_info.get_port_info(self.__port_b)
            self.__port_info_c = self.__dio_info.get_port_info(self.__port_c)

            # Configure the entire port for input.
            self.__dio_device.d_config_port(
                self.__port_a, DigitalDirection.INPUT)

            # Configure the entire port for input.
            self.__dio_device.d_config_port(
                self.__port_b, DigitalDirection.INPUT)

            # Configure the entire port for input.
            self.__dio_device.d_config_port(
                self.__port_c, DigitalDirection.INPUT)

        except Exception as e:
            print('\n', e)
            self._disconnect()

    def read_device(self, a, b, c):
        try:
            # Read each of the bits from the first port.
            for bit_number in a:
                active = not bool(self.__dio_device.d_bit_in(
                    self.__port_a, bit_number))
                self.__update_observer(0, bit_number, active)

            for bit_number in b:
                active = not bool(self.__dio_device.d_bit_in(
                    self.__port_b, bit_number))
                self.__update_observer(1, bit_number, active)

            for bit_number in c:
                active = not bool(self.__dio_device.d_bit_in(
                    self.__port_c, bit_number))
                self.__update_observer(2, bit_number, active)

        except Exception as e:
            print('\n', e)
            self._disconnect()

    def _disconnect(self):
        if self.__daq_device:
            if self.__daq_device.is_connected():
                self.__daq_device.disconnect()
            self.__daq_device.release()

    def __update_observer(self, port, bit, pressed):
        if (self.__lastInputAction[port][bit] != pressed):
            self.__lastInputAction[port][bit] = pressed
            self.__inputActions[port][bit](pressed)
