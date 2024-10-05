from typing import Any, Optional, overload, Type

from pygame.typing import _PathLike

def encode_string(
    obj: Optional[_PathLike],
    encoding: Optional[str] = "unicode_escape",
    errors: Optional[str] = "backslashreplace",
    etype: Optional[Type[Exception]] = UnicodeEncodeError,
) -> bytes: ...
@overload
def encode_file_path(
    obj: Optional[_PathLike], etype: Optional[Type[Exception]] = UnicodeEncodeError
) -> bytes: ...
@overload
def encode_file_path(
    obj: Any, etype: Optional[Type[Exception]] = UnicodeEncodeError
) -> bytes: ...
