"pygame module for interacting with events and queues"

from __future__ import annotations

import gc

from typing import Any, Dict, Type, Union, overload
from pygame.typing import EventLike, IterableLike

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

import pygame as pg


_is_init = False
_custom_event = pg.USEREVENT + 1


def event_name(type: int) -> str:
    """
    event_name(type) -> string

    get the string name from an event id
    """

    if type in _events_map:
        return _events_map[type].__name__
    if pg.USEREVENT <= type < pg.NUMEVENTS:
        return "UserEvent"
    return "Unknown"


def _check_ev_type(ev_type):
    if not isinstance(ev_type, int):
        raise TypeError("event type must be an integer")

    if not 0 <= ev_type < pg.NUMEVENTS:
        raise ValueError("event type out of range")


_events_map: Dict[int, Type["Event"]] = {}


def _unknown_event_factory(ev_type: int) -> Type[Event]:
    if ev_type >= pg.USEREVENT:

        class UserEvent(Event):
            type = ev_type
            _unknown: bool = True

        return UserEvent

    class UnknownEvent(Event):
        type = ev_type
        _unknown: bool = True

    return UnknownEvent


def event_class(type: int) -> type[EventLike]:
    _check_ev_type(type)

    if type not in _events_map:
        _events_map[type] = _unknown_event_factory(type)
    return _events_map[type]


class _EventMeta(type):
    def _create_of_type(cls, type: int, *args, **kwds):
        return event_class(type)(*args, **kwds)

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        if cls is Event:
            return cls._create_of_type(*args, **kwds)
        return super(_EventMeta, cls).__call__(*args, **kwds)


class Event(metaclass=_EventMeta):
    """
    Event(type, dict) -> Event
    Event(type, **attributes) -> Event

    pygame object for representing events
    """

    type: int = -1

    @overload
    def __init__(
        self, type: int, dict: dict[str, Any] | None = None, **kwargs: Any
    ): ...
    @overload
    def __init__(self, dict: dict[str, Any] | None = None, **kwargs: Any): ...

    def __init__(self, *args, **kwargs) -> None:
        self.__init(*args, **kwargs)

    def __init(self, dict: dict[str, Any] | None = None, **kwargs: Any):
        if dict is None:
            dict = kwargs
        else:
            dict.update(kwargs)

        if "type" in dict:
            raise ValueError("redundant type field in event dict")

        self._dict = dict

    def __init_subclass__(cls) -> None:
        if getattr(cls, "type", -1) == -1:
            cls.type = custom_type()
        _events_map[cls.type] = cls

    def __int__(self):
        return self.type

    def __bool__(self):
        return self.type != pg.NOEVENT

    def __eq__(self, other: Any):
        if not isinstance(other, Event):
            return NotImplemented
        return self.type == other.type and self.dict == other.dict

    def __repr__(self):
        if getattr(self, "_unknown", False):
            return (
                f"<{type(self).__module__}.<dynamic>."
                f"{type(self).__name__}({self.type} {self.dict})>"
            )

        return f"<{type(self).__module__}.{type(self).__qualname__}({self.dict})>"

    @property
    def dict(self):
        return self._dict

    def __getattr__(self, name: str) -> Any:
        if name not in self._dict:
            raise AttributeError(
                f"{self.__class__.__name__} object has no attribute {name!r}"
            )
        return self._dict[name]

    def __getattribute__(self, name: str):
        if name == "__dict__":
            return super().__getattribute__("_dict")
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Any):
        if name == "type":
            raise AttributeError(
                "attribute 'type' of 'Event' or its subclass object is protected"
            )

        if name in ("_dict", "dict"):
            super().__setattr__(name, value)
        else:
            self._dict[name] = value

    def __delattr__(self, name: str) -> None:
        del self._dict[name]

    def __dir__(self):
        ret = super().__dir__()
        ret = (*ret, *self._dict.keys())
        return ret


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
    _events_map.clear()
    _events_map.update(_extra_cache)
    _quit()

    _is_init = False


def custom_type():
    """
    custom_type() -> int

    make custom user event type
    """
    global _custom_event

    if _custom_event >= pg.NUMEVENTS:
        raise pg.error("pygame.event.custom_type made too many event types.")

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
    eventtype: int | IterableLike[int],
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

    for ev_type in eventtype:
        _check_ev_type(ev_type)

        if _peek(ev_type) or _peek(_proxify_event_type(ev_type)):
            return True
    return False


_extra_cache = {}


def _create_class(type: int, name: str, note: str | None):
    ret = _EventMeta(name, (Event,), {"type": type, "__doc__": note})
    _extra_cache[type] = ret
    return ret


# To regenerate class definitions:
#   1) Paste class declarations from buildconfig/stubs/pygame/event.pyi above
#   2) Run the code below and paste the output.

# def const_find(vl, guess: str):
#     keys: list[str] = [key for key, value in pg.constants.__dict__.items() if value == vl]
#     if len(keys) < 1:
#         raise ValueError(f"{guess}:{vl} not found int the dict")
#     elif len(keys) == 1:
#         return keys[0]
#     for k in keys:
#         if k.replace("_", "") == guess.upper():
#             return k
#     raise ValueError(f"{guess}:{vl} unresolved: {keys}")

# for cls in _events_map.values():
#     if cls.__name__ == "UserEvent": continue
#     print(
#         f"{cls.__name__} = _create_class(pg.{const_find(cls.type, cls.__name__)}, " \
#         f"{cls.__qualname__!r}, {cls.__doc__!r})"
#     )


ActiveEvent = _create_class(pg.ACTIVEEVENT, "ActiveEvent", None)
AppTerminating = _create_class(pg.APP_TERMINATING, "AppTerminating", None)
AppLowMemory = _create_class(pg.APP_LOWMEMORY, "AppLowMemory", None)
AppWillEnterBackground = _create_class(
    pg.APP_WILLENTERBACKGROUND, "AppWillEnterBackground", None
)
AppDidEnterBackground = _create_class(
    pg.APP_DIDENTERBACKGROUND, "AppDidEnterBackground", None
)
AppWillEnterForeground = _create_class(
    pg.APP_WILLENTERFOREGROUND, "AppWillEnterForeground", None
)
AppDidEnterForeground = _create_class(
    pg.APP_DIDENTERFOREGROUND, "AppDidEnterForeground", None
)
ClipboardUpdate = _create_class(pg.CLIPBOARDUPDATE, "ClipboardUpdate", None)
KeyDown = _create_class(pg.KEYDOWN, "KeyDown", None)
KeyUp = _create_class(pg.KEYUP, "KeyUp", None)
KeyMapChanged = _create_class(pg.KEYMAPCHANGED, "KeyMapChanged", None)
LocaleChanged = _create_class(pg.LOCALECHANGED, "LocaleChanged", "Only for SDL 2.0.14+")
MouseMotion = _create_class(pg.MOUSEMOTION, "MouseMotion", None)
MouseButtonDown = _create_class(pg.MOUSEBUTTONDOWN, "MouseButtonDown", None)
MouseButtonUp = _create_class(pg.MOUSEBUTTONUP, "MouseButtonUp", None)
JoyAxisMotion = _create_class(
    pg.JOYAXISMOTION,
    "JoyAxisMotion",
    'Attribute "joy" is depracated, use "instance_id".',
)
JoyBallMotion = _create_class(
    pg.JOYBALLMOTION,
    "JoyBallMotion",
    'Attribute "joy" is depracated, use "instance_id".',
)
JoyHatMotion = _create_class(
    pg.JOYHATMOTION, "JoyHatMotion", 'Attribute "joy" is depracated, use "instance_id".'
)
JoyButtonUp = _create_class(
    pg.JOYBUTTONUP, "JoyButtonUp", 'Attribute "joy" is depracated, use "instance_id".'
)
JoyButtonDown = _create_class(
    pg.JOYBUTTONDOWN,
    "JoyButtonDown",
    'Attribute "joy" is depracated, use "instance_id".',
)
Quit = _create_class(pg.QUIT, "Quit", None)
SysWMEvent = _create_class(
    pg.SYSWMEVENT,
    "SysWMEvent",
    "\n    Attributes are OS-depended:\n    hwnd, msg, wparam, lparam - Windows.\n"
    "    event - Unix / OpenBSD\n    For other OSes and in some cases for Unix / OpenBSD\n"
    "    this event won't have any attributes.\n    ",
)
VideoResize = _create_class(pg.VIDEORESIZE, "VideoResize", None)
VideoExpose = _create_class(pg.VIDEOEXPOSE, "VideoExpose", None)
MidiIn = _create_class(pg.MIDIIN, "MidiIn", None)
MidiOut = _create_class(pg.MIDIOUT, "MidiOut", None)
NoEvent = _create_class(pg.NOEVENT, "NoEvent", None)
FingerMotion = _create_class(
    pg.FINGERMOTION, "FingerMotion", 'Attribute "window" avalible only for SDL 2.0.14+'
)
FingerDown = _create_class(
    pg.FINGERDOWN, "FingerDown", 'Attribute "window" avalible only for SDL 2.0.14+'
)
FingerUp = _create_class(
    pg.FINGERUP, "FingerUp", 'Attribute "window" avalible only for SDL 2.0.14+'
)
MultiGesture = _create_class(pg.MULTIGESTURE, "MultiGesture", None)
MouseWheel = _create_class(pg.MOUSEWHEEL, "MouseWheel", None)
TextInput = _create_class(pg.TEXTINPUT, "TextInput", None)
TextEditing = _create_class(pg.TEXTEDITING, "TextEditing", None)
DropFile = _create_class(pg.DROPFILE, "DropFile", None)
DropText = _create_class(pg.DROPTEXT, "DropText", None)
DropBegin = _create_class(pg.DROPBEGIN, "DropBegin", None)
DropComplete = _create_class(pg.DROPCOMPLETE, "DropComplete", None)
ControllerAxisMotion = _create_class(
    pg.CONTROLLERAXISMOTION, "ControllerAxisMotion", None
)
ControllerButtonDown = _create_class(
    pg.CONTROLLERBUTTONDOWN, "ControllerButtonDown", None
)
ControllerButtonUp = _create_class(pg.CONTROLLERBUTTONUP, "ControllerButtonUp", None)
ControllerDeviceAdded = _create_class(
    pg.CONTROLLERDEVICEADDED, "ControllerDeviceAdded", None
)
ControllerDeviceRemoved = _create_class(
    pg.CONTROLLERDEVICEREMOVED, "ControllerDeviceRemoved", None
)
ControllerDeviceMapped = _create_class(
    pg.CONTROLLERDEVICEREMAPPED, "ControllerDeviceMapped", None
)
JoyDeviceAdded = _create_class(pg.JOYDEVICEADDED, "JoyDeviceAdded", None)
JoyDeviceRemoved = _create_class(pg.JOYDEVICEREMOVED, "JoyDeviceRemoved", None)
ControllerTouchpadDown = _create_class(
    pg.CONTROLLERTOUCHPADDOWN, "ControllerTouchpadDown", "Only for SDL 2.0.14+"
)
ControllerTouchpadMotion = _create_class(
    pg.CONTROLLERTOUCHPADMOTION, "ControllerTouchpadMotion", "Only for SDL 2.0.14+"
)
ControllerTouchpadUp = _create_class(
    pg.CONTROLLERTOUCHPADUP, "ControllerTouchpadUp", "Only for SDL 2.0.14+"
)
ControllerSensorUpdate = _create_class(
    pg.CONTROLLERSENSORUPDATE, "ControllerSensorUpdate", "Only for SDL 2.0.14+"
)
AudioDeviceAdded = _create_class(pg.AUDIODEVICEADDED, "AudioDeviceAdded", None)
AudioDeviceRemoved = _create_class(pg.AUDIODEVICEREMOVED, "AudioDeviceRemoved", None)
RenderTargetsReset = _create_class(pg.RENDER_TARGETS_RESET, "RenderTargetsReset", None)
RenderDeviceReset = _create_class(pg.RENDER_DEVICE_RESET, "RenderDeviceReset", None)
WindowShown = _create_class(pg.WINDOWSHOWN, "WindowShown", None)
WindowHidden = _create_class(pg.WINDOWHIDDEN, "WindowHidden", None)
WindowExposed = _create_class(pg.WINDOWEXPOSED, "WindowExposed", None)
WindowMoved = _create_class(pg.WINDOWMOVED, "WindowMoved", None)
WindowResized = _create_class(pg.WINDOWRESIZED, "WindowResized", None)
WindowSizeChanged = _create_class(pg.WINDOWSIZECHANGED, "WindowSizeChanged", None)
WindowMinimized = _create_class(pg.WINDOWMINIMIZED, "WindowMinimized", None)
WindowMaximized = _create_class(pg.WINDOWMAXIMIZED, "WindowMaximized", None)
WindowRestored = _create_class(pg.WINDOWRESTORED, "WindowRestored", None)
WindowEnter = _create_class(pg.WINDOWENTER, "WindowEnter", None)
WindowLeave = _create_class(pg.WINDOWLEAVE, "WindowLeave", None)
WindowFocusGained = _create_class(pg.WINDOWFOCUSGAINED, "WindowFocusGained", None)
WindowFocusLost = _create_class(pg.WINDOWFOCUSLOST, "WindowFocusLost", None)
WindowClose = _create_class(pg.WINDOWCLOSE, "WindowClose", None)
WindowTakeFocus = _create_class(pg.WINDOWTAKEFOCUS, "WindowTakeFocus", None)
WindowHitTest = _create_class(pg.WINDOWHITTEST, "WindowHitTest", None)
WindowICCProfChanged = _create_class(
    pg.WINDOWICCPROFCHANGED, "WindowICCProfChanged", None
)
WindowDisplayChanged = _create_class(
    pg.WINDOWDISPLAYCHANGED, "WindowDisplayChanged", None
)


class UserEvent(Event):
    """
    User defined event. To create your own, subclass Event instead.
    You can test if an event is UserEvent by calling:
        isinstance(event, pygame.event.UserEvent)
    """

    type: int = pg.USEREVENT

    def __instancecheck__(self, instance: Any, /) -> bool:
        return (
            isinstance(instance, Event) and pg.USEREVENT <= instance.type < pg.NUMEVENTS
        )


_extra_cache[pg.USEREVENT] = UserEvent


__all__ = [
    "Event",
    "EventType",
    "event_class",
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
    "ActiveEvent",
    "AppTerminating",
    "AppLowMemory",
    "AppWillEnterBackground",
    "AppDidEnterBackground",
    "AppWillEnterForeground",
    "AppDidEnterForeground",
    "ClipboardUpdate",
    "KeyDown",
    "KeyUp",
    "KeyMapChanged",
    "LocaleChanged",
    "MouseMotion",
    "MouseButtonDown",
    "MouseButtonUp",
    "JoyAxisMotion",
    "JoyBallMotion",
    "JoyHatMotion",
    "JoyButtonUp",
    "JoyButtonDown",
    "Quit",
    "SysWMEvent",
    "VideoResize",
    "VideoExpose",
    "MidiIn",
    "MidiOut",
    "NoEvent",
    "FingerMotion",
    "FingerDown",
    "FingerUp",
    "MultiGesture",
    "MouseWheel",
    "TextInput",
    "TextEditing",
    "DropFile",
    "DropText",
    "DropBegin",
    "DropComplete",
    "ControllerAxisMotion",
    "ControllerButtonDown",
    "ControllerButtonUp",
    "ControllerDeviceAdded",
    "ControllerDeviceRemoved",
    "ControllerDeviceMapped",
    "JoyDeviceAdded",
    "JoyDeviceRemoved",
    "ControllerTouchpadDown",
    "ControllerTouchpadMotion",
    "ControllerTouchpadUp",
    "ControllerSensorUpdate",
    "AudioDeviceAdded",
    "AudioDeviceRemoved",
    "RenderTargetsReset",
    "RenderDeviceReset",
    "WindowShown",
    "WindowHidden",
    "WindowExposed",
    "WindowMoved",
    "WindowResized",
    "WindowSizeChanged",
    "WindowMinimized",
    "WindowMaximized",
    "WindowRestored",
    "WindowEnter",
    "WindowLeave",
    "WindowFocusGained",
    "WindowFocusLost",
    "WindowClose",
    "WindowTakeFocus",
    "WindowHitTest",
    "WindowICCProfChanged",
    "WindowDisplayChanged",
    "UserEvent",
]
