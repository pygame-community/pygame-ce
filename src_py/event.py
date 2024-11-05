from __future__ import annotations

from pygame._event import *  # pylint: disable=wildcard-import,unused-wildcard-import; lgtm[py/polluting-import]
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
    if USEREVENT <= type < NUMEVENTS:
        return "UserEvent"
    return "Unknown"


class Event:
    """
    Event(type, dict) -> Event
    Event(type, **attributes) -> Event
    pygame object for representing events
    """

    type: int
    dict: dict[str, ...]

    def __init__(self, type: int, dict: dict[str, ...] | None = None, **kwargs):
        if not isinstance(type, int):
            raise TypeError("event type must be an integer")

        if not 0 <= type < NUMEVENTS:
            raise ValueError("event type out of range")

        dict = dict if dict is not None else {}
        dict.update(kwargs)

        if "type" in dict:
            raise ValueError("redundant type field in event dict")

        self._type = type
        self._dict = dict

    def __new__(cls, *args, **kwargs):
        if "type" in kwargs:
            raise ValueError("redundant type field in event dict")
        return super().__new__(cls)

    def __int__(self):
        return self.type

    def __bool__(self):
        return self.type != pg.NOEVENT

    def __eq__(self, other: Event):
        if not isinstance(other, Event):
            return NotImplemented
        return self.type == other.type and self.dict == other.dict

    def __repr__(self):
        return f"<Event({self.type}-{event_name(self.type)} {self.dict})"

    @property
    def dict(self):
        return self._dict

    @property
    def type(self):
        return self._type

    def __getattr__(self, name):
        return self._dict[name]

    def __getattribute__(self, name):
        if name == "__dict__":
            return super().__getattribute__("_dict")
        return super().__getattribute__(name)

    def __setattr__(self, name, value):
        if name in ("_type", "_dict", "type", "dict"):
            super().__setattr__(name, value)
        else:
            self._dict[name] = value


EventType = Event
register_event_class(Event)


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
