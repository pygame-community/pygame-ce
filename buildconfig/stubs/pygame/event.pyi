from typing import Any, Dict, Type, Optional, Union, overload

from pygame.typing import SequenceLike, EventLike
from pygame import Window, constants as _c


class Event(EventLike):
    type: int

    @overload
    def __init__(
        self, type: int, dict: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> None: ...
    @overload
    def __init__(
        self, dict: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> None: ...

    def __getattribute__(self, name: str) -> Any: ...
    def __setattr__(self, name: str, value: Any) -> None: ...
    def __delattr__(self, name: str) -> None: ...
    def __int__(self) -> int: ...
    def __bool__(self) -> bool: ...
    def __eq__(self, other: Any) -> bool: ...

_EventTypes = Union[int, SequenceLike[int]]

def pump() -> None: ...
def get(
    eventtype: Optional[_EventTypes] = None,
    pump: Any = True,
    exclude: Optional[_EventTypes] = None,
) -> list[EventLike]: ...
def poll() -> EventLike: ...
def wait(timeout: int = 0) -> EventLike: ...
def peek(eventtype: _EventTypes, pump: Any = True) -> Union[bool, EventLike]: ...
def clear(eventtype: Optional[_EventTypes] = None, pump: Any = True) -> None: ...
def event_name(type: int) -> str: ...
def set_blocked(type: Optional[_EventTypes], *args: int) -> None: ...
def set_allowed(type: Optional[_EventTypes], *args: int) -> None: ...
def get_blocked(type: _EventTypes, *args: int) -> bool: ...
def set_grab(grab: bool, /) -> None: ...
def get_grab() -> bool: ...
def post(event: EventLike, /) -> bool: ...
def custom_type() -> int: ...
def event_class(type: int) -> Type[Event]: ...
def init() -> None: ...
def quit() -> None: ...

EventType = Event

# BEGIN Event subclasses
class ActiveEvent(Event):
    type: int = _c.ACTIVEEVENT
    gain: int
    state: int

class AppTerminating(Event):
    type: int = _c.APP_TERMINATING

class AppLowMemory(Event):
    type: int = _c.APP_LOWMEMORY

class AppWillEnterBackground(Event):
    type: int = _c.APP_WILLENTERBACKGROUND

class AppDidEnterBackground(Event):
    type: int = _c.APP_DIDENTERBACKGROUND

class AppWillEnterForeground(Event):
    type: int = _c.APP_WILLENTERFOREGROUND

class AppDidEnterForeground(Event):
    type: int = _c.APP_DIDENTERFOREGROUND

class ClipboardUpdate(Event):
    type: int = _c.CLIPBOARDUPDATE

class KeyDown(Event):
    type: int = _c.KEYDOWN
    unicode: str
    key: int
    mod: int
    scancode: int
    window: Optional[Window]

class KeyUp(Event):
    type: int = _c.KEYUP
    unicode: str
    key: int
    mod: int
    scancode: int
    window: Optional[Window]

class KeyMapChanged(Event):
    type: int = _c.KEYMAPCHANGED

class LocaleChanged(Event):
    """Only for SDL 2.0.14+"""
    type: int = _c.LOCALECHANGED

class MouseMotion(Event):
    type: int = _c.MOUSEMOTION
    pos: tuple[int, int]
    rel: tuple[int, int]
    buttons: tuple[int, int, int]
    touch: bool
    window: Optional[Window]

class MouseButtonDown(Event):
    type: int = _c.MOUSEBUTTONDOWN
    pos: tuple[int, int]
    button: int
    touch: bool
    window: Optional[Window]

class MouseButtonUp(Event):
    type: int = _c.MOUSEBUTTONUP
    pos: tuple[int, int]
    button: int
    touch: bool
    window: Optional[Window]

class JoyAxisMotion(Event):
    """Attribute "joy" is depracated, use "instance_id"."""
    type: int = _c.JOYAXISMOTION
    joy: int
    instance_id: int
    axis: int
    value: float

class JoyBallMotion(Event):
    """Attribute "joy" is depracated, use "instance_id"."""
    type: int = _c.JOYBALLMOTION
    joy: int
    instance_id: int
    ball: int
    rel: tuple[int, int]

class JoyHatMotion(Event):
    """Attribute "joy" is depracated, use "instance_id"."""
    type: int = _c.JOYHATMOTION
    joy: int
    instance_id: int
    hat: int
    value: tuple[int, int]

class JoyButtonUp(Event):
    """Attribute "joy" is depracated, use "instance_id"."""
    type: int = _c.JOYBUTTONUP
    joy: int
    instance_id: int
    button: int

class JoyButtonDown(Event):
    """Attribute "joy" is depracated, use "instance_id"."""
    type: int = _c.JOYBUTTONDOWN
    joy: int
    instance_id: int
    button: int

class Quit(Event):
    type: int = _c.QUIT

class SysWMEvent(Event):
    """
    Attributes are OS-depended:
    hwnd, msg, wparam, lparam - Windows.
    event - Unix / OpenBSD
    For other OSes and in some cases for Unix / OpenBSD
    this event won't have any attributes.
    """
    type: int = _c.SYSWMEVENT
    hwnd: int
    msg: int
    wparam: int
    lparam: int
    event: bytes

class VideoResize(Event):
    type: int = _c.VIDEORESIZE
    size: tuple[int, int]
    w: int
    h: int

class VideoExpose(Event):
    type: int = _c.VIDEOEXPOSE

class MidiIn(Event):
    type: int = _c.MIDIIN

class MidiOut(Event):
    type: int = _c.MIDIOUT

class NoEvent(Event):
    type: int = _c.NOEVENT

class FingerMotion(Event):
    """Attribute "window" avalible only for SDL 2.0.14+"""
    type: int = _c.FINGERMOTION
    touch_id: int
    finger_id: int
    x: float
    y: float
    dx: float
    dy: float
    pressure: float
    window: Optional[Window]

class FingerDown(Event):
    """Attribute "window" avalible only for SDL 2.0.14+"""
    type: int = _c.FINGERDOWN
    touch_id: int
    finger_id: int
    x: float
    y: float
    dx: float
    dy: float
    pressure: float
    window: Optional[Window]

class FingerUp(Event):
    """Attribute "window" avalible only for SDL 2.0.14+"""
    type: int = _c.FINGERUP
    touch_id: int
    finger_id: int
    x: float
    y: float
    dx: float
    dy: float
    pressure: float
    window: Optional[Window]

class MultiGesture(Event):
    type: int = _c.MULTIGESTURE
    touch_id: int
    x: float
    y: float
    rotated: float
    pinched: float
    num_fingers: int

class MouseWheel(Event):
    type: int = _c.MOUSEWHEEL
    flipped: bool
    x: int
    y: int
    precise_x: float
    precise_y: float
    touch: bool
    window: Optional[Window]

class TextInput(Event):
    type: int = _c.TEXTINPUT
    text: str
    window: Optional[Window]

class TextEditing(Event):
    type: int = _c.TEXTEDITING
    text: str
    start: int
    length: int
    window: Optional[Window]

class DropFile(Event):
    type: int = _c.DROPFILE
    file: str
    window: Optional[Window]

class DropText(Event):
    type: int = _c.DROPTEXT
    text: str
    window: Optional[Window]

class DropBegin(Event):
    type: int = _c.DROPBEGIN
    window: Optional[Window]

class DropComplete(Event):
    type: int = _c.DROPCOMPLETE
    window: Optional[Window]

class ControllerAxisMotion(Event):
    type: int = _c.CONTROLLERAXISMOTION
    instance_id: int
    axis: int
    value: int

class ControllerButtonDown(Event):
    type: int = _c.CONTROLLERBUTTONDOWN
    instance_id: int
    button: int

class ControllerButtonUp(Event):
    type: int = _c.CONTROLLERBUTTONUP
    instance_id: int
    button: int

class ControllerDeviceAdded(Event):
    type: int = _c.CONTROLLERDEVICEADDED
    device_index: int
    guid: str

class ControllerDeviceRemoved(Event):
    type: int = _c.CONTROLLERDEVICEREMOVED
    instance_id: int

class ControllerDeviceMapped(Event):
    type: int = _c.CONTROLLERDEVICEREMAPPED
    instance_id: int

class JoyDeviceAdded(Event):
    type: int = _c.JOYDEVICEADDED
    device_index: int
    guid: str

class JoyDeviceRemoved(Event):
    type: int = _c.JOYDEVICEREMOVED
    instance_id: int

class ControllerTouchpadDown(Event):
    """Only for SDL 2.0.14+"""
    type: int = _c.CONTROLLERTOUCHPADDOWN
    instance_id: int
    touch_id: int
    finger_id: int
    x: float
    y: float
    pressure: float

class ControllerTouchpadMotion(Event):
    """Only for SDL 2.0.14+"""
    type: int = _c.CONTROLLERTOUCHPADMOTION
    instance_id: int
    touch_id: int
    finger_id: int
    x: float
    y: float
    pressure: float

class ControllerTouchpadUp(Event):
    """Only for SDL 2.0.14+"""
    type: int = _c.CONTROLLERTOUCHPADUP
    instance_id: int
    touch_id: int
    finger_id: int
    x: float
    y: float
    pressure: float

class ControllerSensorUpdate(Event):
    """Only for SDL 2.0.14+"""
    type: int = _c.CONTROLLERSENSORUPDATE

class AudioDeviceAdded(Event):
    type: int = _c.AUDIODEVICEADDED
    which: int
    iscapture: int

class AudioDeviceRemoved(Event):
    type: int = _c.AUDIODEVICEREMOVED
    which: int
    iscapture: int

class RenderTargetsReset(Event):
    type: int = _c.RENDER_TARGETS_RESET

class RenderDeviceReset(Event):
    type: int = _c.RENDER_DEVICE_RESET

class WindowShown(Event):
    type: int = _c.WINDOWSHOWN
    window: Optional[Window]

class WindowHidden(Event):
    type: int = _c.WINDOWHIDDEN
    window: Optional[Window]

class WindowExposed(Event):
    type: int = _c.WINDOWEXPOSED
    window: Optional[Window]

class WindowMoved(Event):
    type: int = _c.WINDOWMOVED
    x: int
    y: int
    window: Optional[Window]

class WindowResized(Event):
    type: int = _c.WINDOWRESIZED
    x: int
    y: int
    window: Optional[Window]

class WindowSizeChanged(Event):
    type: int = _c.WINDOWSIZECHANGED
    x: int
    y: int
    window: Optional[Window]

class WindowMinimized(Event):
    type: int = _c.WINDOWMINIMIZED
    window: Optional[Window]

class WindowMaximized(Event):
    type: int = _c.WINDOWMAXIMIZED
    window: Optional[Window]

class WindowRestored(Event):
    type: int = _c.WINDOWRESTORED
    window: Optional[Window]

class WindowEnter(Event):
    type: int = _c.WINDOWENTER
    window: Optional[Window]

class WindowLeave(Event):
    type: int = _c.WINDOWLEAVE
    window: Optional[Window]

class WindowFocusGained(Event):
    type: int = _c.WINDOWFOCUSGAINED
    window: Optional[Window]

class WindowFocusLost(Event):
    type: int = _c.WINDOWFOCUSLOST
    window: Optional[Window]

class WindowClose(Event):
    type: int = _c.WINDOWCLOSE
    window: Optional[Window]

class WindowTakeFocus(Event):
    type: int = _c.WINDOWTAKEFOCUS
    window: Optional[Window]

class WindowHitTest(Event):
    type: int = _c.WINDOWHITTEST
    window: Optional[Window]

class WindowICCProfChanged(Event):
    type: int = _c.WINDOWICCPROFCHANGED
    window: Optional[Window]

class WindowDisplayChanged(Event):
    type: int = _c.WINDOWDISPLAYCHANGED
    display_index: int
    window: Optional[Window]

class UserEvent(Event):
    type: int = _c.USEREVENT

# END Event subclasses
