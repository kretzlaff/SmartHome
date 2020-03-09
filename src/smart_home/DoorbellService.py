#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import datetime

import soco

from rx import Observable
from rx import operators as ops
from rx.scheduler import EventLoopScheduler


class DoorbellService(object):
    def __init__(self):
        self.__scheduler = EventLoopScheduler()
        self.__lastPlayed = datetime.datetime.now()

    def __play(self):
        if (datetime.datetime.now() -
                self.__lastPlayed).total_seconds() < 5.0:
            return

        # Pass in the IP of your Sonos speaker
        sonos = soco.SoCo('192.168.50.2')

        # Pass in a URI to a media file to have it streamed through the Sonos
        sonos.play_uri('http://192.168.50.135:8080/doorbell.mp3')
        self.__lastPlayed = datetime.datetime.now()

    def addSwitch(self, observable: Observable):
        # Add a handler to the switch state
        observable.pipe(ops.filter(lambda active: active is True),
                        ops.observe_on(self.__scheduler)).subscribe(
            lambda active: self.__play())
