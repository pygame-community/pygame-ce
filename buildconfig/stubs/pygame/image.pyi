from typing import Optional, Tuple, Union

from pygame.bufferproxy import BufferProxy
from pygame.surface import Surface

from ._common import FileArg, Literal, IntCoordinate, Coordinate

_BufferStyle = Union[BufferProxy, bytes, bytearray, memoryview]
_to_bytes_format = Literal[
    "P", "RGB", "RGBX", "RGBA", "ARGB", "BGRA", "ABGR", "RGBA_PREMULT", "ARGB_PREMULT"
]
_from_buffer_format = Literal["P", "RGB", "BGR", "BGRA", "RGBX", "RGBA", "ARGB"]
_from_bytes_format = Literal["P", "RGB", "RGBX", "RGBA", "ARGB", "BGRA", "ABGR"]

def load(file: FileArg, namehint: str = "") -> Surface: ...
def load_sized_svg(file: FileArg, size: Coordinate) -> Surface: ...
def save(surface: Surface, file: FileArg, namehint: str = "") -> None: ...
def get_sdl_image_version(linked: bool = True) -> Optional[Tuple[int, int, int]]: ...
def get_extended() -> bool: ...
def tobytes(
    surface: Surface,
    format: _to_bytes_format,
    flipped: bool = False,
    pitch: int = -1,
) -> bytes: ...
def frombytes(
    bytes: bytes,
    size: IntCoordinate,
    format: _from_bytes_format,
    flipped: bool = False,
    pitch: int = -1,
) -> Surface: ...
def frombuffer(
    bytes: _BufferStyle,
    size: IntCoordinate,
    format: _from_buffer_format,
    pitch: int = -1,
) -> Surface: ...
def load_basic(file: FileArg, /) -> Surface: ...
def load_extended(file: FileArg, namehint: str = "") -> Surface: ...
def save_extended(surface: Surface, file: FileArg, namehint: str = "") -> None: ...
# tostring deprecated since 2.3.0
# fromstring deprecated since 2.3.0
