from os import PathLike as PathProtocol
from typing import IO, Callable, Tuple, Union, TypeVar, Protocol, SupportsIndex

PathLike = Union[str, bytes, PathProtocol[str], PathProtocol[bytes]]
FileLike = Union[PathLike, IO[bytes], IO[str]]

_T = TypeVar("_T", covariant=True)

class SequenceLike(Protocol[_T]):
    """
    Variant of the standard `Sequence` ABC that only requires `__getitem__` and `__len__`.
    """
    def __getitem__(self, __i: SupportsIndex) -> _T: ...
    def __len__(self) -> int: ...

# Right now, it isn't possible to annotate sizes (popular tools don't support it) but
# when it is, the below types should be appropriately annotated
CoordinateLike = SequenceLike[float] # floats are supported even if integers are usually expected
IntCoordinateLike = SequenceLike[int] # integers are strictly required

RGBALike = Tuple[int, int, int, int]
ColorLike = Union[int, str, SequenceLike[int]]

_CanBeRect = SequenceLike[Union[float, CoordinateLike]]

class _HasRectAttribute(Protocol):
    # An object that has a rect attribute that is either a rect, or a function
    # that returns a rect confirms to the rect protocol
    rect: Union["RectLike", Callable[[], "RectLike"]]

RectLike = Union[_CanBeRect, _HasRectAttribute]
