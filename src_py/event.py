"pygame module for interacting with events and queues"

from __future__ import annotations

import gc

from typing import Any, Union
from .typing import EventLike, IterableLike

from pygame._event import (
    _internal_mod_init as _init,
    _internal_mod_quit as _quit,
    pump as _pump,
    register_event_class as _register_event_class,
    allowed_get as _allowed_get,
    allowed_set as _allowed_set,
    video_check as _video_check,
    post,
    get_grab,
    set_grab,
    wait,
    poll,
    _get,
    _peek,
    _proxify_event_type,
)

from pygame.base import error
import pygame as pg


_is_init = False
_custom_event = pg.USEREVENT + 1
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
    """
    event_name(type) -> string

    get the string name from an event id
    """

    if type in _NAMES_MAPPING:
        return _NAMES_MAPPING[type]
    if pg.USEREVENT <= type < pg.NUMEVENTS:
        return "UserEvent"
    return "Unknown"


def _check_ev_type(ev_type):
    if not isinstance(ev_type, int):
        raise TypeError("event type must be an integer")

    if not 0 <= ev_type < pg.NUMEVENTS:
        raise ValueError("event type out of range")


class Event:
    """
    Event(type, dict) -> Event
    Event(type, **attributes) -> Event

    pygame object for representing events
    """

    def __init__(self, type: int, dict: dict[str, Any] | None = None, **kwargs: Any):
        _check_ev_type(type)

        if dict is None:
            dict = kwargs
        else:
            dict.update(kwargs)

        if "type" in dict:
            raise ValueError("redundant type field in event dict")

        self._type = type
        self._dict = dict

    def __new__(cls, *args: Any, **kwargs: Any):
        if "type" in kwargs:
            raise ValueError("redundant type field in event dict")
        return super().__new__(cls)

    def __int__(self):
        return self.type

    def __bool__(self):
        return self.type != pg.NOEVENT

    def __eq__(self, other: Any):
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

    def __getattr__(self, name: str) -> Any:
        return self._dict[name]

    def __getattribute__(self, name: str):
        if name == "__dict__":
            return super().__getattribute__("_dict")
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Any):
        if name in ("_type", "_dict", "type", "dict"):
            super().__setattr__(name, value)
        else:
            self._dict[name] = value

    def __delattr__(self, name: str) -> None:
        del self._dict[name]


EventType = Event
_register_event_class(Event)


def init():
    global _is_init

    _init()

    _is_init = True


def quit():
    global _is_init, _custom_event

    # Clear event queue to avoid memory leak when SDL tries to clear it
    # without freeing our resources.
    clear(pump=False)

    # The main reason for _custom_event to be reset here is
    # so we can have a unit test that checks if pygame.event.custom_type() stops
    # returning new types when they are finished,
    # without that test preventing further tests from getting a custom event type.
    _custom_event = pg.USEREVENT + 1
    _quit()

    _is_init = False


def custom_type():
    """
    custom_type() -> int

    make custom user event type
    """
    global _custom_event

    if _custom_event >= pg.NUMEVENTS:
        raise error("pygame.event.custom_type made too many event types.")

    _custom_event += 1
    return _custom_event - 1


def pump():
    """
    pump() -> None

    internally process pygame event handlers
    """
    return _pump(True)


def _parse(type: int | IterableLike[int], args: tuple[int, ...]) -> list[int]:
    types = []

    types: list[int] = []

    if isinstance(type, int):
        types.append(type)
    else:
        types.extend(iter(type))

    if args:
        types.extend(args)

    return types


def _setter(val: bool, type: int | IterableLike[int] | None, *args: int):
    if type is None:
        if args:
            raise ValueError("Args aren't supported for type==None.")
        for ev in range(pg.NUMEVENTS):
            _allowed_set(ev, val)
        return

    for t in _parse(type, args):
        _check_ev_type(t)
        _allowed_set(t, val)


def set_blocked(type: int | IterableLike[int] | None, *args: int):
    """
    set_blocked(type: int, *args) -> None
    set_blocked(type: list) -> None
    set_blocked(None) -> None

    control which events are blocked on the queue
    """

    _setter(False, type, *args)


def set_allowed(type: int | IterableLike[int] | None, *args: int):
    """
    set_allowed(type: int, *args) -> None
    set_allowed(type: list) -> None
    set_allowed(None) -> None

    control which events are allowed on the queue
    """

    _setter(True, type, *args)


def get_blocked(type: int | IterableLike[int], *args: int):
    """
    get_blocked(type: int, *args) -> bool
    get_blocked(type: list) -> bool

    test if a type of event is blocked from the queue
    """

    for t in _parse(type, args):
        _check_ev_type(t)
        if not _allowed_get(t):
            return True
    return False


def clear(eventtype: int | IterableLike[int] | None = None, pump: bool = True):
    """
    clear(eventtype=None) -> None
    clear(eventtype=None, pump=True) -> None

    remove all events from the queue
    """
    if eventtype is None or isinstance(eventtype, int):
        get(eventtype, pump)
    else:
        get(list(iter(eventtype)), pump)

    gc.collect()


def _get_many(
    ev_type: int, to: list | None = None, proxify: bool = True
) -> list[EventLike]:
    if to is None:
        to = []

    ev = _get(ev_type)

    while ev:
        to.append(ev)
        ev = _get(ev_type)

    if proxify:
        to = _get_many(_proxify_event_type(ev_type), to, False)

    return to


def get(
    eventtype: int | IterableLike[int] | None = None,
    pump: bool = True,
    exclude: int | IterableLike[int] | None = None,
) -> list[EventLike]:
    """
    get(eventtype=None) -> Eventlist
    get(eventtype=None, pump=True) -> Eventlist
    get(eventtype=None, pump=True, exclude=None) -> Eventlist

    get events from the queue
    """
    _video_check()
    _pump(pump)

    if isinstance(eventtype, int):
        eventtype = [eventtype]

    if isinstance(exclude, int):
        exclude = [exclude]

    if eventtype is None:
        if exclude is None:
            # Get all events
            return _get_many(-1, proxify=False)

        # Get all events except
        excluded = []

        for ev_type in exclude:
            _check_ev_type(ev_type)
            _get_many(ev_type, excluded)

        ret = _get_many(-1, proxify=False)

        for ev in excluded:
            post(ev)

        del excluded
        return ret

    if exclude is not None:
        raise pg.error("Invalid combination of excluded and included event type")

    # Get all events of type
    ret = []

    for ev_type in eventtype:
        _check_ev_type(ev_type)
        _get_many(ev_type, ret)

    return ret


def peek(
    eventtype: int | IterableLike[int] | None = None,
    pump: bool = True,
) -> Union[EventLike, bool]:
    """
    peek() -> Event instance
    peek(eventtype) -> bool
    peek(eventtype, pump=True) -> bool

    test if event types are waiting on the queue
    """
    _video_check()
    _pump(pump)

    if isinstance(eventtype, int):
        eventtype = [eventtype]

    if eventtype is None:
        # Can't seek without mutating event queue here,
        # Due to PgEvent_New being a destructive operation.
        ret = _get(-1)

        if ret is None:
            return Event(0)

        post(ret)
        return ret

    for ev_type in eventtype:
        _check_ev_type(ev_type)

        if _peek(ev_type) or _peek(_proxify_event_type(ev_type)):
            return True
    return False


__all__ = [
    "Event",
    "EventType",
    "pump",
    "get",
    "poll",
    "wait",
    "peek",
    "clear",
    "event_name",
    "set_blocked",
    "set_allowed",
    "get_blocked",
    "set_grab",
    "get_grab",
    "post",
    "custom_type",
    "init",
    "quit",
]
