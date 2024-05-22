from typing import (
    Any,
    Dict,
    List,
    Tuple,
    Optional,
    Union,
    Literal,
    overload,
    Type,
)

from pygame._common import Sequence
from pygame.window import Window

class _EventMeta(type): ...

class Event(metaclass=_EventMeta):
    type: int
    dict: Dict[str, Any]
    __dict__: Dict[str, Any]
    __hash__: None  # type: ignore
    @overload
    def __init__(
        self, type: int, dict: Dict[str, Any] = ..., /, **kwargs: Any
    ) -> None: ...
    @overload
    def __init__(
        self, dict: Dict[str, Any] = ..., /, **kwargs: Any
    ) -> None: ...
    def __getattribute__(self, name: str) -> Any: ...
    def __setattr__(self, name: str, value: Any) -> None: ...
    def __delattr__(self, name: str) -> None: ...
    def __bool__(self) -> bool: ...

class ActiveEvent(Event):
    type: Literal[32768] = 32768
    gain: int
    state: int

class AppTerminating(Event):
    type: Literal[257] = 257

class AppLowMemory(Event):
    type: Literal[258] = 258

class AppWillEnterBackground(Event):
    type: Literal[259] = 259

class AppDidEnterBackground(Event):
    type: Literal[260] = 260

class AppWillEnterForeground(Event):
    type: Literal[261] = 261

class AppDidEnterForeground(Event):
    type: Literal[262] = 262

class ClipboardUpdate(Event):
    type: Literal[2304] = 2304

class KeyDown(Event):
    type: Literal[768] = 768
    unicode: str
    key: int
    mod: int
    scancode: int
    window: Optional[Window]

class KeyUp(Event):
    type: Literal[769] = 769
    unicode: str
    key: int
    mod: int
    scancode: int
    window: Optional[Window]

class KeyMapChanged(Event):
    type: Literal[772] = 772

class LocaleChanged(Event):
    """Only for SDL 2.0.14+"""
    type: Literal[263] = 263

class MouseMotion(Event):
    type: Literal[1024] = 1024
    pos: Tuple[int, int]
    rel: Tuple[int, int]
    buttons: tuple[int, int, int]
    touch: bool
    window: Optional[Window]

class MouseButtonDown(Event):
    type: Literal[1025] = 1025
    pos: Tuple[int, int]
    button: int
    touch: bool
    window: Optional[Window]

class MouseButtonUp(Event):
    type: Literal[1026] = 1026
    pos: Tuple[int, int]
    button: int
    touch: bool
    window: Optional[Window]

class JoyAxisMotion(Event):
    type: Literal[1536] = 1536
    joy: int
    instance_id: int
    axis: int
    value: float

class JoyBallMotion(Event):
    type: Literal[1537] = 1537
    joy: int
    instance_id: int
    ball: int
    rel: Tuple[int, int]

class JoyHatMotion(Event):
    type: Literal[1538] = 1538
    joy: int
    instance_id: int
    hat: int
    value: Tuple[int, int]

class JoyButtonUp(Event):
    type: Literal[1540] = 1540
    joy: int
    instance_id: int
    button: int

class JoyButtonDown(Event):
    type: Literal[1539] = 1539
    joy: int
    instance_id: int
    button: int

class Quit(Event):
    type: Literal[256] = 256

class SysWMEvent(Event):
    """
    Attributes are OS-depended:
    hwnd, msg, wparam, lparam - Windows.
    event - Unix / OpenBSD
    For other OSes and in some cases for Unix / OpenBSD
    this event won't have any attributes.
    """
    type: Literal[513] = 513
    hwnd: int
    msg: int
    wparam: int
    lparam: int
    event: bytes

class VideoResize(Event):
    type: Literal[32769] = 32769
    size: Tuple[int, int]
    w: int
    h: int

class VideoExpose(Event):
    type: Literal[32770] = 32770

class MidiIn(Event):
    type: Literal[32771] = 32771

class MidiOut(Event):
    type: Literal[32772] = 32772

class NoEvent(Event):
    type: Literal[0] = 0

class FingerMotion(Event):
    """Attribute "window" avalible only for SDL 2.0.14+"""
    type: Literal[1794] = 1794
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
    type: Literal[1792] = 1792
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
    type: Literal[1793] = 1793
    touch_id: int
    finger_id: int
    x: float
    y: float
    dx: float
    dy: float
    pressure: float
    window: Optional[Window]

class MultiGesture(Event):
    type: Literal[2050] = 2050
    touch_id: int
    x: float
    y: float
    rotated: float
    pinched: float
    num_fingers: int

class MouseWheel(Event):
    type: Literal[1027] = 1027
    flipped: bool
    x: int
    y: int
    precise_x: float
    precise_y: float
    touch: bool
    window: Optional[Window]

class TextInput(Event):
    type: Literal[771] = 771
    text: str
    window: Optional[Window]

class TextEditing(Event):
    type: Literal[770] = 770
    text: str
    start: int
    length: int
    window: Optional[Window]

class DropFile(Event):
    type: Literal[4096] = 4096
    file: str
    window: Optional[Window]

class DropText(Event):
    type: Literal[4097] = 4097
    text: str
    window: Optional[Window]

class DropBegin(Event):
    type: Literal[4098] = 4098
    window: Optional[Window]

class DropComplete(Event):
    type: Literal[4099] = 4099
    window: Optional[Window]

class ControllerAxisMotion(Event):
    type: Literal[1616] = 1616
    instance_id: int
    axis: int
    value: int

class ControllerButtonDown(Event):
    type: Literal[1617] = 1617
    instance_id: int
    button: int

class ControllerButtonUp(Event):
    type: Literal[1618] = 1618
    instance_id: int
    button: int

class ControllerDeviceAdded(Event):
    type: Literal[1619] = 1619
    device_index: int
    guid: str

class ControllerDeviceRemoved(Event):
    type: Literal[1620] = 1620
    instance_id: int

class ControllerDeviceMapped(Event):
    type: Literal[1621] = 1621
    instance_id: int

class JoyDeviceAdded(Event):
    type: Literal[1541] = 1541
    device_index: int
    guid: str

class JoyDeviceRemoved(Event):
    type: Literal[1542] = 1542
    instance_id: int

class ControllerTouchpadDown(Event):
    """Only for SDL 2.0.14+"""
    type: Literal[1622] = 1622
    instance_id: int
    touch_id: int
    finger_id: int
    x: float
    y: float
    pressure: float

class ControllerTouchpadMotion(Event):
    """Only for SDL 2.0.14+"""
    type: Literal[1623] = 1623
    instance_id: int
    touch_id: int
    finger_id: int
    x: float
    y: float
    pressure: float

class ControllerTouchpadUp(Event):
    """Only for SDL 2.0.14+"""
    type: Literal[1624] = 1624
    instance_id: int
    touch_id: int
    finger_id: int
    x: float
    y: float
    pressure: float

class ControllerSensorUpdate(Event):
    """Only for SDL 2.0.14+"""
    type: Literal[1625] = 1625

class AudioDeviceAdded(Event):
    type: Literal[4352] = 4352
    which: int
    iscapture: int

class AudioDeviceRemoved(Event):
    type: Literal[4353] = 4353
    which: int
    iscapture: int

class RenderTargetsReset(Event):
    type: Literal[8192] = 8192

class RenderDeviceReset(Event):
    type: Literal[8193] = 8193

class WindowShown(Event):
    type: Literal[32774] = 32774
    window: Optional[Window]

class WindowHidden(Event):
    type: Literal[32775] = 32775
    window: Optional[Window]

class WindowExposed(Event):
    type: Literal[32776] = 32776
    window: Optional[Window]

class WindowMoved(Event):
    type: Literal[32777] = 32777
    x: int
    y: int
    window: Optional[Window]

class WindowResized(Event):
    type: Literal[32778] = 32778
    x: int
    y: int
    window: Optional[Window]

class WindowSizeChanged(Event):
    type: Literal[32779] = 32779
    x: int
    y: int
    window: Optional[Window]

class WindowMinimized(Event):
    type: Literal[32780] = 32780
    window: Optional[Window]

class WindowMaximized(Event):
    type: Literal[32781] = 32781
    window: Optional[Window]

class WindowRestored(Event):
    type: Literal[32782] = 32782
    window: Optional[Window]

class WindowEnter(Event):
    type: Literal[32783] = 32783
    window: Optional[Window]

class WindowLeave(Event):
    type: Literal[32784] = 32784
    window: Optional[Window]

class WindowFocusGained(Event):
    type: Literal[32785] = 32785
    window: Optional[Window]

class WindowFocusLost(Event):
    type: Literal[32786] = 32786
    window: Optional[Window]

class WindowClose(Event):
    type: Literal[32787] = 32787
    window: Optional[Window]

class WindowTakeFocus(Event):
    type: Literal[32788] = 32788
    window: Optional[Window]

class WindowHitTest(Event):
    type: Literal[32789] = 32789
    window: Optional[Window]

class WindowICCProfChanged(Event):
    type: Literal[32790] = 32790
    window: Optional[Window]

class WindowDisplayChanged(Event):
    type: Literal[32791] = 32791
    display_index: int
    window: Optional[Window]

_EventTypes = Union[int, Sequence[int]]

def pump() -> None: ...
def get(
    eventtype: Optional[_EventTypes] = None,
    pump: Any = True,
    exclude: Optional[_EventTypes] = None,
) -> List[Event]: ...
def poll() -> Event: ...
def wait(timeout: int = 0) -> Event: ...
def peek(eventtype: Optional[_EventTypes] = None, pump: Any = True) -> bool: ...
def clear(eventtype: Optional[_EventTypes] = None, pump: Any = True) -> None: ...
def event_name(type: int, /) -> str: ...
def set_blocked(type: Optional[_EventTypes], /) -> None: ...
def set_allowed(type: Optional[_EventTypes], /) -> None: ...
def get_blocked(type: _EventTypes, /) -> bool: ...
def set_grab(grab: bool, /) -> None: ...
def get_grab() -> bool: ...
def post(event: Event, /) -> bool: ...
def custom_type() -> int: ...
def event_class(type: int, /) -> Type[Event]: ...
def __dir__() -> List[str]: ...
def __getattr__(name: str, /) -> object: ...

EventType = Event
