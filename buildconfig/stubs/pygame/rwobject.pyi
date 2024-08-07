from typing import Any, Optional, overload, Type

from pygame.typing import PathLike

def encode_string(
    obj: Optional[PathLike],
    encoding: Optional[str] = "unicode_escape",
    errors: Optional[str] = "backslashreplace",
    etype: Optional[Type[Exception]] = UnicodeEncodeError,
) -> bytes: ...
@overload
def encode_file_path(
    obj: Optional[PathLike], etype: Optional[Type[Exception]] = UnicodeEncodeError
) -> bytes: ...
@overload
def encode_file_path(
    obj: Any, etype: Optional[Type[Exception]] = UnicodeEncodeError
) -> bytes: ...
