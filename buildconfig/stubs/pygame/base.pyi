from collections.abc import Callable
from typing import Any

__version__: str

class error(RuntimeError): ...
class BufferError(Exception): ...

# Always defined
HAVE_NEWBUF: int = 1

def init() -> tuple[int, int]: ...
def quit() -> None: ...
def get_init() -> bool: ...
def get_error() -> str: ...
def set_error(error_msg: str, /) -> None: ...
def get_sdl_version(linked: bool = True) -> tuple[int, int, int]: ...
def get_sdl_byteorder() -> int: ...
def register_quit(callable: Callable[[], Any], /) -> None: ...

# undocumented part of pygame API, kept here to make stubtest happy
def get_array_interface(arg: Any, /) -> dict: ...
