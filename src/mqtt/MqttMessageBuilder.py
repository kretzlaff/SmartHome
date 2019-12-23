
import json


def getTurnOffPayload():
    return json.dumps({
        "state": "OFF",
        "transition": 3
    })


def getTurnOnPayload():
    return json.dumps({
        "state": "ON",
        "transition": 3
    })


def getTogglePayload():
    return json.dumps({
        "state": "TOGGLE",
        "transition": 3
    })


def getChangeBrightnessPayload(brightness):
    return json.dumps({
        "brightness": brightness,
        "transition": 0
    })


def getChangeTempPayload(temp):
    return json.dumps({
        "color_temp": temp,
        "transition": 0
    })


def getChangeColorPayload(r, g, b):
    return json.dumps({
        "color": {
            "r": r,
            "g": g,
            "b": b
        },
        "transition": 0
    })


def getBlinkPayload():
    return json.dumps({
        "alert": "select",
        "transition": 0
    })


def getLongBlinkPayload():
    return json.dumps({
        "alert": "lselect",
        "transition": 0
    })


def getStopBlinkPayload():
    return json.dumps({
        "alert": "none",
        "transition": 0
    })
