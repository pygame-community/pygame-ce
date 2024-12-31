"""Sample app run by mypy to ensure typing.py aliases work as expected"""

from pygame import typing
import pygame
import pathlib


# validate SequenceLike
class MySequence:
    def __getitem__(self, index: int) -> str:
        if index > 20:
            raise IndexError()
        if index % 2 == 0:
            return "a"
        return "bc"

    def __len__(self) -> int:
        return 20

def validator_SequenceLike(sequence: typing.SequenceLike) -> int:
    return 0

def validator_SequenceLikeTypes(
    sequence_float: typing.SequenceLike[float],
    sequence_int: typing.SequenceLike[int],
    sequence_str: typing.SequenceLike[str],
    sequence_sequence: typing.SequenceLike[typing.SequenceLike],
) -> int:
    return 0

# must pass
validator_SequenceLike(MySequence())
validator_SequenceLike([0, 1, 2, 3])
validator_SequenceLike((0, 1, 2, 3))
validator_SequenceLike(pygame.Rect(-10, 10, 40, 40))
validator_SequenceLike(pygame.Vector2())
validator_SequenceLike("1234567890")

validator_SequenceLikeTypes(
    (-1.5, -0.5, 0, 0.5, 2.5, 10),
    (-2, -1, 0, 1, 2, 3),
    "abcdefghijklmnopqrstuvwxyz",
    [(0.5, 1.5), (-1, 1), "123", [(), (), ()]],
)


# validate _PathLike
class MyPath:
    def __fspath__(self) -> str:
        return "file.py"

def validator_PathLike(path: typing._PathLike) -> int:
    return 0

# must pass
validator_PathLike("file.py")
validator_PathLike(b"file.py")
validator_PathLike(pathlib.Path("file.py"))
validator_PathLike(MyPath())


# validate Point, IntPoint
def validator_Point(point: typing.Point) -> int:
    return 0

def validator_IntPoint(point: typing.IntPoint) -> int:
    return 0

# must pass
validator_Point((1, 2))
validator_Point([3, -4])
validator_Point((5, -6.5))
validator_Point((-6.7, 8.9))
validator_Point(pygame.Vector2())

validator_IntPoint((3, 4))
validator_IntPoint([-4, -3])


def validator_ColorLike(color: typing.ColorLike) -> int:
    return 0

# must pass
validator_ColorLike("green")
validator_ColorLike(1)
validator_ColorLike((255, 255, 255, 30))
validator_ColorLike(pygame.Color(100, 100, 100, 100))


# validate RectLike
class MyObject1:
    def __init__(self):
        self.rect = pygame.Rect(10, 10, 20, 20)

class MyObject2:
    def __init__(self):
        self.rect = lambda: pygame.Rect(5, 5, 10, 10)

class MyObject3:
    def rect(self) -> pygame.Rect:
        return pygame.Rect(15, 15, 30, 30)

def validator_RectLike(rect: typing.RectLike) -> int:
    return 0

# must pass
validator_RectLike((10, 10, 10, 10))
validator_RectLike(((5, 5), (30, 30)))
validator_RectLike(([3, 3.2], pygame.Vector2()))
validator_RectLike(pygame.Rect(1, 2, 3, 4))
validator_RectLike(MyObject1())
validator_RectLike(MyObject2())
validator_RectLike(MyObject3())
