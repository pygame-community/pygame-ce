from pygame._event import *  # pylint: disable=wildcard-import; lgtm[py/polluting-import]
from pygame._event import _internal_mod_init as _init, _internal_mod_quit as _quit
from pygame.constants import USEREVENT, NUMEVENTS
from pygame.base import error


_is_init = False
_custom_event = USEREVENT + 1
_NAMES_MAPPING = {
    32768: "ActiveEvent",
    257: "AppTerminating",
    258: "AppLowMemory",
    259: "AppWillEnterBackground",
    260: "AppDidEnterBackground",
    261: "AppWillEnterForeground",
    262: "AppDidEnterForeground",
    2304: "ClipboardUpdate",
    768: "KeyDown",
    769: "KeyUp",
    772: "KeyMapChanged",
    263: "LocaleChanged",
    1024: "MouseMotion",
    1025: "MouseButtonDown",
    1026: "MouseButtonUp",
    1536: "JoyAxisMotion",
    1537: "JoyBallMotion",
    1538: "JoyHatMotion",
    1540: "JoyButtonUp",
    1539: "JoyButtonDown",
    256: "Quit",
    513: "SysWMEvent",
    32769: "VideoResize",
    32770: "VideoExpose",
    32771: "MidiIn",
    32772: "MidiOut",
    0: "NoEvent",
    1794: "FingerMotion",
    1792: "FingerDown",
    1793: "FingerUp",
    2050: "MultiGesture",
    1027: "MouseWheel",
    771: "TextInput",
    770: "TextEditing",
    4096: "DropFile",
    4097: "DropText",
    4098: "DropBegin",
    4099: "DropComplete",
    1616: "ControllerAxisMotion",
    1617: "ControllerButtonDown",
    1618: "ControllerButtonUp",
    1619: "ControllerDeviceAdded",
    1620: "ControllerDeviceRemoved",
    1621: "ControllerDeviceMapped",
    1541: "JoyDeviceAdded",
    1542: "JoyDeviceRemoved",
    1622: "ControllerTouchpadDown",
    1623: "ControllerTouchpadMotion",
    1624: "ControllerTouchpadUp",
    1625: "ControllerSensorUpdate",
    4352: "AudioDeviceAdded",
    4353: "AudioDeviceRemoved",
    8192: "RenderTargetsReset",
    8193: "RenderDeviceReset",
    32774: "WindowShown",
    32775: "WindowHidden",
    32776: "WindowExposed",
    32777: "WindowMoved",
    32778: "WindowResized",
    32779: "WindowSizeChanged",
    32780: "WindowMinimized",
    32781: "WindowMaximized",
    32782: "WindowRestored",
    32783: "WindowEnter",
    32784: "WindowLeave",
    32785: "WindowFocusGained",
    32786: "WindowFocusLost",
    32787: "WindowClose",
    32788: "WindowTakeFocus",
    32789: "WindowHitTest",
    32790: "WindowICCProfChanged",
    32791: "WindowDisplayChanged",
}


def event_name(type: int):
    if type in _NAMES_MAPPING:
        return _NAMES_MAPPING[type]
    elif type >= USEREVENT and type < NUMEVENTS:
        return "UserEvent"
    return "Unknown"


# class Event:
#     def __init__(self, type: int):
#         self.type = type


def init():
    global _is_init

    _init()

    _is_init = True


def quit():
    global _is_init, _custom_event

    # The main reason for _custom_event to be reset here is
    # so we can have a unit test that checks if pygame.event.custom_type() stops
    # returning new types when they are finished,
    # without that test preventing further tests from getting a custom event type.
    _custom_event = USEREVENT + 1
    _quit()

    _is_init = False


def custom_type():
    """custom_type() -> int\nmake custom user event type"""
    global _custom_event

    if _custom_event < NUMEVENTS:
        _custom_event += 1
        return _custom_event - 1
    else:
        raise error("pygame.event.custom_type made too many event types.")
