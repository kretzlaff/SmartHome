#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from soco import SoCo


class SonosClient(object):
    def __init__(self):
        sonos = SoCo('Living Room')  # Pass in the IP of your Sonos speaker
        # You could use the discover function instead, if you don't know the IP

        # Pass in a URI to a media file to have it streamed through the Sonos
        # speaker
        sonos.play_uri(
            'http://ia801402.us.archive.org/20/items/TenD2005-07-16.flac16/TenD2005-07-16t10Wonderboy.mp3')

        track = sonos.get_current_track_info()

        sonos.pause()

        # Play a stopped or paused track
        sonos.play()


a = SonosClient()
