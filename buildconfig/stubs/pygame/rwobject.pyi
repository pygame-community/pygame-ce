from typing import Any, Optional, overload

from pygame.typing import _PathLike

def encode_string(
    obj: Optional[_PathLike],
    encoding: Optional[str] = "unicode_escape",
    errors: Optional[str] = "backslashreplace",
    etype: Optional[type[Exception]] = UnicodeEncodeError,
) -> bytes: ...
@overload
def encode_file_path(
    obj: Optional[_PathLike], etype: Optional[type[Exception]] = UnicodeEncodeError
) -> bytes: ...
@overload
def encode_file_path(
    obj: Any, etype: Optional[type[Exception]] = UnicodeEncodeError
) -> bytes: ...
