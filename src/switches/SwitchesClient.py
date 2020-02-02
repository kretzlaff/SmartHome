#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from __future__ import print_function
from rx.subject import Subject

from uldaq import get_daq_device_inventory, DaqDevice, InterfaceType, DigitalPortIoType, DigitalDirection


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

            # Create the DAQ device object associated with the specified descriptor index.
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

            # If the port is bit configurable, then configure the individual bits
            # for input; otherwise, configure the entire port for input.
            if self.__port_info_a.port_io_type == DigitalPortIoType.BITIO:
                # Configure all of the bits for input for the first port.
                for i in range(self.__port_info_a.number_of_bits):
                    self.__dio_device.d_config_bit(
                        self.__port_a, i, DigitalDirection.INPUT)
            elif self.__port_info_a.port_io_type == DigitalPortIoType.IO:
                # Configure the entire port for input.
                self.__dio_device.d_config_port(
                    self.__port_a, DigitalDirection.INPUT)

            if self.__port_info_b.port_io_type == DigitalPortIoType.BITIO:
                # Configure all of the bits for input for the first port.
                for i in range(self.__port_info_b.number_of_bits):
                    self.__dio_device.d_config_bit(
                        self.__port_b, i, DigitalDirection.INPUT)
            elif self.__port_info_b.port_io_type == DigitalPortIoType.IO:
                # Configure the entire port for input.
                self.__dio_device.d_config_port(
                    self.__port_b, DigitalDirection.INPUT)

            if self.__port_info_c.port_io_type == DigitalPortIoType.BITIO:
                # Configure all of the bits for input for the first port.
                for i in range(self.__port_info_c.number_of_bits):
                    self.__dio_device.d_config_bit(
                        self.__port_c, i, DigitalDirection.INPUT)
            elif self.__port_info_c.port_io_type == DigitalPortIoType.IO:
                # Configure the entire port for input.
                self.__dio_device.d_config_port(
                    self.__port_c, DigitalDirection.INPUT)

        except Exception as e:
            print('\n', e)
            self._disconnect()

    def read_device(self):
        try:
            # Read each of the bits from the first port.
            for bit_number in range(self.__port_info_a.number_of_bits):
                active = not bool(self.__dio_device.d_bit_in(
                    self.__port_a, bit_number))
                self.__update_observer(self.__device_id, 0, bit_number, active)

            for bit_number in range(self.__port_info_b.number_of_bits):
                active = not bool(self.__dio_device.d_bit_in(
                    self.__port_b, bit_number))
                self.__update_observer(self.__device_id, 1, bit_number, active)

            for bit_number in range(self.__port_info_c.number_of_bits):
                active = not bool(self.__dio_device.d_bit_in(
                    self.__port_c, bit_number))
                self.__update_observer(self.__device_id, 2, bit_number, active)

        except Exception as e:
            print('\n', e)
            self._disconnect()

    def _disconnect(self):
        if self.__daq_device:
            if self.__daq_device.is_connected():
                self.__daq_device.disconnect()
            self.__daq_device.release()

    def __update_observer(self, device, port, bit, pressed):
        if port == 0:
            if bit == 0:
                # print('+++ ' + self.__device_id + ' A0')
                self._A0.on_next(pressed)
            if bit == 1:
                # print('+++ ' + self.__device_id + ' A1')
                self._A1.on_next(pressed)
            if bit == 2:
                # print('+++ ' + self.__device_id + ' A2')
                self._A2.on_next(pressed)
            if bit == 3:
                # print('+++ ' + self.__device_id + ' A3')
                self._A3.on_next(pressed)
            if bit == 4:
                # print('+++ ' + self.__device_id + ' A4')
                self._A4.on_next(pressed)
            if bit == 5:
                # print('+++ ' + self.__device_id + ' A5')
                self._A5.on_next(pressed)
            if bit == 6:
                # print('+++ ' + self.__device_id + ' A6')
                self._A6.on_next(pressed)
            if bit == 7:
                # print('+++ ' + self.__device_id + ' A7')
                self._A7.on_next(pressed)
        if port == 1:
            if bit == 0:
                # print('+++ ' + self.__device_id + ' B0')
                self._B0.on_next(pressed)
            if bit == 1:
                # print('+++ ' + self.__device_id + ' B1')
                self._B1.on_next(pressed)
            if bit == 2:
                # print('+++ ' + self.__device_id + ' B2')
                self._B2.on_next(pressed)
            if bit == 3:
                # print('+++ ' + self.__device_id + ' B3')
                self._B3.on_next(pressed)
            if bit == 4:
                # print('+++ ' + self.__device_id + ' B4')
                self._B4.on_next(pressed)
            if bit == 5:
                # print('+++ ' + self.__device_id + ' B5')
                self._B5.on_next(pressed)
            if bit == 6:
                # print('+++ ' + self.__device_id + ' B6')
                self._B6.on_next(pressed)
            if bit == 7:
                # print('+++ ' + self.__device_id + ' B7')
                self._B7.on_next(pressed)
        if port == 2:
            if bit == 0:
                # print('+++ ' + self.__device_id + ' C0')
                self._C0.on_next(pressed)
            if bit == 1:
                # print('+++ ' + self.__device_id + ' C1')
                self._C1.on_next(pressed)
            if bit == 2:
                # print('+++ ' + self.__device_id + ' C2')
                self._C2.on_next(pressed)
            if bit == 3:
                # print('+++ ' + self.__device_id + ' C3')
                self._C3.on_next(pressed)
            if bit == 4:
                # print('+++ ' + self.__device_id + ' C4')
                self._C4.on_next(pressed)
            if bit == 5:
                # print('+++ ' + self.__device_id + ' C5')
                self._C5.on_next(pressed)
            if bit == 6:
                # print('+++ ' + self.__device_id + ' C6')
                self._C6.on_next(pressed)
            if bit == 7:
                # print('+++ ' + self.__device_id + ' C7')
                self._C7.on_next(pressed)
