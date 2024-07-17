from pygame._event import *  # pylint: disable=wildcard-import; lgtm[py/polluting-import]
from pygame._event import _internal_mod_init as _init, _internal_mod_quit as _quit
from pygame.constants import USEREVENT, NUMEVENTS
from pygame.base import error
import pygame as pg


_is_init = False
_custom_event = USEREVENT + 1
_NAMES_MAPPING = {
    pg.ACTIVEEVENT: "ActiveEvent",
    pg.APP_TERMINATING: "AppTerminating",
    pg.APP_LOWMEMORY: "AppLowMemory",
    pg.APP_WILLENTERBACKGROUND: "AppWillEnterBackground",
    pg.APP_DIDENTERBACKGROUND: "AppDidEnterBackground",
    pg.APP_WILLENTERFOREGROUND: "AppWillEnterForeground",
    pg.APP_DIDENTERFOREGROUND: "AppDidEnterForeground",
    pg.CLIPBOARDUPDATE: "ClipboardUpdate",
    pg.KEYDOWN: "KeyDown",
    pg.KEYUP: "KeyUp",
    pg.KEYMAPCHANGED: "KeyMapChanged",
    pg.LOCALECHANGED: "LocaleChanged",
    pg.MOUSEMOTION: "MouseMotion",
    pg.MOUSEBUTTONDOWN: "MouseButtonDown",
    pg.MOUSEBUTTONUP: "MouseButtonUp",
    pg.JOYAXISMOTION: "JoyAxisMotion",
    pg.JOYBALLMOTION: "JoyBallMotion",
    pg.JOYHATMOTION: "JoyHatMotion",
    pg.JOYBUTTONUP: "JoyButtonUp",
    pg.JOYBUTTONDOWN: "JoyButtonDown",
    pg.QUIT: "Quit",
    pg.SYSWMEVENT: "SysWMEvent",
    pg.VIDEORESIZE: "VideoResize",
    pg.VIDEOEXPOSE: "VideoExpose",
    pg.MIDIIN: "MidiIn",
    pg.MIDIOUT: "MidiOut",
    pg.NOEVENT: "NoEvent",
    pg.FINGERMOTION: "FingerMotion",
    pg.FINGERDOWN: "FingerDown",
    pg.FINGERUP: "FingerUp",
    pg.MULTIGESTURE: "MultiGesture",
    pg.MOUSEWHEEL: "MouseWheel",
    pg.TEXTINPUT: "TextInput",
    pg.TEXTEDITING: "TextEditing",
    pg.DROPFILE: "DropFile",
    pg.DROPTEXT: "DropText",
    pg.DROPBEGIN: "DropBegin",
    pg.DROPCOMPLETE: "DropComplete",
    pg.CONTROLLERAXISMOTION: "ControllerAxisMotion",
    pg.CONTROLLERBUTTONDOWN: "ControllerButtonDown",
    pg.CONTROLLERBUTTONUP: "ControllerButtonUp",
    pg.CONTROLLERDEVICEADDED: "ControllerDeviceAdded",
    pg.CONTROLLERDEVICEREMOVED: "ControllerDeviceRemoved",
    pg.CONTROLLERDEVICEREMAPPED: "ControllerDeviceMapped",
    pg.JOYDEVICEADDED: "JoyDeviceAdded",
    pg.JOYDEVICEREMOVED: "JoyDeviceRemoved",
    pg.CONTROLLERTOUCHPADDOWN: "ControllerTouchpadDown",
    pg.CONTROLLERTOUCHPADMOTION: "ControllerTouchpadMotion",
    pg.CONTROLLERTOUCHPADUP: "ControllerTouchpadUp",
    pg.CONTROLLERSENSORUPDATE: "ControllerSensorUpdate",
    pg.AUDIODEVICEADDED: "AudioDeviceAdded",
    pg.AUDIODEVICEREMOVED: "AudioDeviceRemoved",
    pg.RENDER_TARGETS_RESET: "RenderTargetsReset",
    pg.RENDER_DEVICE_RESET: "RenderDeviceReset",
    pg.WINDOWSHOWN: "WindowShown",
    pg.WINDOWHIDDEN: "WindowHidden",
    pg.WINDOWEXPOSED: "WindowExposed",
    pg.WINDOWMOVED: "WindowMoved",
    pg.WINDOWRESIZED: "WindowResized",
    pg.WINDOWSIZECHANGED: "WindowSizeChanged",
    pg.WINDOWMINIMIZED: "WindowMinimized",
    pg.WINDOWMAXIMIZED: "WindowMaximized",
    pg.WINDOWRESTORED: "WindowRestored",
    pg.WINDOWENTER: "WindowEnter",
    pg.WINDOWLEAVE: "WindowLeave",
    pg.WINDOWFOCUSGAINED: "WindowFocusGained",
    pg.WINDOWFOCUSLOST: "WindowFocusLost",
    pg.WINDOWCLOSE: "WindowClose",
    pg.WINDOWTAKEFOCUS: "WindowTakeFocus",
    pg.WINDOWHITTEST: "WindowHitTest",
    pg.WINDOWICCPROFCHANGED: "WindowICCProfChanged",
    pg.WINDOWDISPLAYCHANGED: "WindowDisplayChanged",
}


def event_name(type: int) -> str:
    if type in _NAMES_MAPPING:
        return _NAMES_MAPPING[type]
    elif USEREVENT <= type < NUMEVENTS:
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

    if _custom_event >= NUMEVENTS:
        raise error("pygame.event.custom_type made too many event types.")

    _custom_event += 1
    return _custom_event - 1
