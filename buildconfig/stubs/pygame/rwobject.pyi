from typing import Any, overload

from pygame.typing import _PathLike

def encode_string(
    obj: _PathLike | None,
    encoding: str | None = "unicode_escape",
    errors: str | None = "backslashreplace",
    etype: type[Exception] | None = UnicodeEncodeError,
) -> bytes: ...
@overload
def encode_file_path(
    obj: _PathLike | None, etype: type[Exception] | None = UnicodeEncodeError
) -> bytes: ...
@overload
def encode_file_path(
    obj: Any, etype: type[Exception] | None = UnicodeEncodeError
) -> bytes: ...
