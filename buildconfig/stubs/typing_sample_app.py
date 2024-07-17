"""
Sample app run by mypy to ensure typing.py aliases work as expected
"""
from pygame import typing
import pygame

# validate SequenceLike
class MySequence:
    def __getitem__(self, index):
        if index > 20:
            raise IndexError()
        if index % 2 == 0:
            return 1
        return 0
    
    def __len__(self):
        return 20
    
def validator_SequenceLike(sequence: typing.SequenceLike) -> int:
    return 0

# must pass
validator_SequenceLike(MySequence())
validator_SequenceLike([0, 1, 2, 3])
validator_SequenceLike((0, 1, 2, 3))
validator_SequenceLike(pygame.Rect(-10, 10, 40, 40))
validator_SequenceLike(pygame.Vector2())
validator_SequenceLike("1234567890")

# validate PathLike
class MyPath:
    def __fspath__(self) -> str:
        return "file.py"
    
def validator_PathLike(path: typing.PathLike) -> int:
    return 0

# must pass
validator_PathLike("file.py")
validator_PathLike(b"file.py")
validator_PathLike(MyPath())

# validate CoordinateLike, IntCoordinateLike

def validator_CoordinateLike(coordinate: typing.CoordinateLike) -> int:
    return 0

def validator_IntCoordinateLike(coordinate: typing.IntCoordinateLike) -> int:
    return 0

# must pass
validator_CoordinateLike((1, 2))
validator_CoordinateLike([3, -4])
validator_CoordinateLike((5, -6.5))
validator_CoordinateLike((-6.7, 8.9))
validator_CoordinateLike(pygame.Vector2())

validator_IntCoordinateLike((3, 4))
validator_IntCoordinateLike([-4, -3])

# validate RGBALike, ColorLike
def validator_RGBALike(rgba: typing.RGBALike) -> int:
    return 0

def validator_ColorLike(color: typing.ColorLike) -> int:
    return 0

# must pass
validator_RGBALike((100, 200, 50, 20))
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
    
def validator_RectLike(rect: typing.RectLike) -> int:
    return 0

# must pass
validator_RectLike((10, 10, 10, 10))
validator_RectLike(((5, 5), (30, 30)))
validator_RectLike(pygame.Rect(1, 2, 3, 4))
validator_RectLike(MyObject1())
validator_RectLike(MyObject2())
