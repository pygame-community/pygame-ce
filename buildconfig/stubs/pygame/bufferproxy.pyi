from typing import Any, Dict, overload

class BufferProxy:
    parent: Any
    length: int
    raw: bytes
    __array_interface__: Dict[str, Any]
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, parent: Any) -> None: ...
    def write(self, buffer: bytes, offset: int = 0) -> None: ...
