from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
    Literal,
    overload,
    Type,
)

from ._common import Sequence

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
        self, type: int, dict: Dict[str, Any] = ..., /, **kwargs: Any
    ) -> None: ...
    def __getattribute__(self, name: str) -> Any: ...
    def __setattr__(self, name: str, value: Any) -> None: ...
    def __delattr__(self, name: str) -> None: ...
    def __bool__(self) -> bool: ...

# TODO: fill with arguments.

class ActiveEvent(Event):
    type: Literal[32768] = 32768

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

class KeyUp(Event):
    type: Literal[769] = 769

class KeyMapChanged(Event):
    type: Literal[772] = 772

class LocaleChanged(Event):
    """Only for SDL 2.0.14+"""
    type: Literal[263] = 263

class MouseMotion(Event):
    type: Literal[1024] = 1024

class MouseButtonDown(Event):
    type: Literal[1025] = 1025

class MouseButtonUp(Event):
    type: Literal[1026] = 1026

class JoyAxisMotion(Event):
    type: Literal[1536] = 1536

class JoyBallMotion(Event):
    type: Literal[1537] = 1537

class JoyHatMotion(Event):
    type: Literal[1538] = 1538

class JoyButtonUp(Event):
    type: Literal[1540] = 1540

class JoyButtonDown(Event):
    type: Literal[1539] = 1539

class Quit(Event):
    type: Literal[256] = 256

class SysWMEvent(Event):
    type: Literal[513] = 513

class VideoResize(Event):
    type: Literal[32769] = 32769

class VideoExpose(Event):
    type: Literal[32770] = 32770

class MidiIn(Event):
    type: Literal[32771] = 32771

class MidiOut(Event):
    type: Literal[32772] = 32772

class NoEvent(Event):
    type: Literal[0] = 0

class FingerMotion(Event):
    type: Literal[1794] = 1794

class FingerDown(Event):
    type: Literal[1792] = 1792

class FingerUp(Event):
    type: Literal[1793] = 1793

class MultiGesture(Event):
    type: Literal[2050] = 2050

class MouseWheel(Event):
    type: Literal[1027] = 1027

class TextInput(Event):
    type: Literal[771] = 771

class TextEditing(Event):
    type: Literal[770] = 770

class DropFile(Event):
    type: Literal[4096] = 4096

class DropText(Event):
    type: Literal[4097] = 4097

class DropBegin(Event):
    type: Literal[4098] = 4098

class DropComplete(Event):
    type: Literal[4099] = 4099

class ControllerAxisMotion(Event):
    type: Literal[1616] = 1616

class ControllerButtonDown(Event):
    type: Literal[1617] = 1617

class ControllerButtonUp(Event):
    type: Literal[1618] = 1618

class ControllerDeviceAdded(Event):
    type: Literal[1619] = 1619

class ControllerDeviceRemoved(Event):
    type: Literal[1620] = 1620

class ControllerDeviceMapped(Event):
    type: Literal[1621] = 1621

class JoyDeviceAdded(Event):
    type: Literal[1541] = 1541

class JoyDeviceRemoved(Event):
    type: Literal[1542] = 1542

class ControllerTouchpadDown(Event):
    """Only for SDL 2.0.14+"""
    type: Literal[1622] = 1622

class ControllerTouchpadMotion(Event):
    """Only for SDL 2.0.14+"""
    type: Literal[1623] = 1623

class ControllerTouchpadUp(Event):
    """Only for SDL 2.0.14+"""
    type: Literal[1624] = 1624

class ControllerSensorUpdate(Event):
    """Only for SDL 2.0.14+"""
    type: Literal[1625] = 1625

class AudioDeviceAdded(Event):
    type: Literal[4352] = 4352

class AudioDeviceRemoved(Event):
    type: Literal[4353] = 4353

class RenderTargetsReset(Event):
    type: Literal[8192] = 8192

class RenderDeviceReset(Event):
    type: Literal[8193] = 8193

class WindowShown(Event):
    type: Literal[32774] = 32774

class WindowHidden(Event):
    type: Literal[32775] = 32775

class WindowExposed(Event):
    type: Literal[32776] = 32776

class WindowMoved(Event):
    type: Literal[32777] = 32777

class WindowResized(Event):
    type: Literal[32778] = 32778

class WindowSizeChanged(Event):
    type: Literal[32779] = 32779

class WindowMinimized(Event):
    type: Literal[32780] = 32780

class WindowMaximized(Event):
    type: Literal[32781] = 32781

class WindowRestored(Event):
    type: Literal[32782] = 32782

class WindowEnter(Event):
    type: Literal[32783] = 32783

class WindowLeave(Event):
    type: Literal[32784] = 32784

class WindowFocusGained(Event):
    type: Literal[32785] = 32785

class WindowFocusLost(Event):
    type: Literal[32786] = 32786

class WindowClose(Event):
    type: Literal[32787] = 32787

class WindowTakeFocus(Event):
    type: Literal[32788] = 32788

class WindowHitTest(Event):
    type: Literal[32789] = 32789

class WindowICCProfChanged(Event):
    type: Literal[32790] = 32790

class WindowDisplayChanged(Event):
    type: Literal[32791] = 32791

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
