import numpy
from pygame.mixer import Sound
from typing_extensions import deprecated  # added in 3.13

def array(sound: Sound) -> numpy.ndarray: ...
def samples(sound: Sound) -> numpy.ndarray: ...
def make_sound(array: numpy.ndarray) -> Sound: ...
@deprecated("Only numpy is supported")
def use_arraytype(arraytype: str) -> None: ...
@deprecated("Only numpy is supported")
def get_arraytype() -> str: ...
@deprecated("Only numpy is supported")
def get_arraytypes() -> tuple[str]: ...

# keep in sync with sndarray.py
__all__ = [
    "array",
    "samples",
    "make_sound",
    "use_arraytype",
    "get_arraytype",
    "get_arraytypes",
]
