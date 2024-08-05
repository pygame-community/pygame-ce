from os import PathLike
from typing import IO, Callable, Tuple, Union, TypeVar, Protocol, SupportsIndex

# For functions that take a file name
AnyPath = Union[str, bytes, PathLike[str], PathLike[bytes]]

# Most pygame functions that take a file argument should be able to handle
# a FileArg type
FileArg = Union[AnyPath, IO[bytes], IO[str]]

_T = TypeVar("_T", covariant=True)

class Sequence(Protocol[_T]):
    """
    This is different from the standard python 'Sequence' abc. This is used in places
    where only __getitem__ and __len__ is actually needed (basically almost all places
    where a sequence is used). The standard 'Sequence' abc has some extra methods.
    """
    def __getitem__(self, __i: SupportsIndex) -> _T: ...
    def __len__(self) -> int: ...

# Right now, it isn't possible to annotate sizes (popular tools don't support it) but
# when it is, the below types should be appropriately annotated

# Yes, float. The reason being, pygame handles float without erroring in a lot of places
# where a coordinate is expected (usually by rounding to int).
# Also, 'Union[int, float] == float'
Coordinate = Sequence[float]

# This is used in places where ints are strictly required
IntCoordinate = Sequence[int]

# This typehint is used when a function would return an RGBA tuple
RGBAOutput = Tuple[int, int, int, int]
ColorValue = Union[int, str, Sequence[int]]

_CanBeRect = Sequence[Union[float, Coordinate]]

class _HasRectAttribute(Protocol):
    # An object that has a rect attribute that is either a rect, or a function
    # that returns a rect confirms to the rect protocol
    rect: Union[RectValue, Callable[[], RectValue]]

RectValue = Union[_CanBeRect, _HasRectAttribute]

"""
# testing code
def a(b: Coordinate):
    b[0]
    b[1]
    len(b)
    e1, e2 = b
    for i in b:
        i -= 1


import numpy
from pygame import Vector2

class MyAmoger:
    def __init__(self):
        pass

    def __getitem__(self, index):
        if index not in (0, 1):
            raise IndexError()

        return 42 if index else 69

    def __len__(self):
        return 2


# should pass
a([1, 2])
a([4.2, 5.2])
a((1, 2))
a((1.4, 2.8))
a(MyAmoger())
a(range(2, 4))  # yes, range object is a 'Sequence'
a(numpy.array([1.3, 2.1]))
a(b"ab")  # weird but this actually works in code (this represents (97, 98) btw)
a(bytearray([1, 2]))
a(Vector2())

print("Done testing the passes!")

# should technically error, but right now we can't annotate sizes so they pass on
# type testing
a([1, 2, 3])
a([4.2, 5.2, 2, 4])
a((1,))
a(numpy.array([1.3, 2.1, 4.2]))

# all of the below should always error
a({})
a({1: 2})
a("abc")
a({1, 2})

"""
