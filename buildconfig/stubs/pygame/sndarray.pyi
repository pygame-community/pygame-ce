"""Pygame module for accessing sound sample data.

Functions to convert between NumPy arrays and Sound objects. This
module will only be functional when pygame can use the external NumPy
package. If NumPy can't be imported, ``sndarray`` becomes a ``MissingModule``
object.

Sound data is made of thousands of samples per second, and each sample is the
amplitude of the wave at a particular moment in time. For example, in 22-kHz
format, element number 5 of the array is the amplitude of the wave after
5/22000 seconds.

The arrays are indexed by the ``X`` axis first, followed by the ``Y`` axis.
Each sample is an 8-bit or 16-bit integer, depending on the data format. A
stereo sound file has two values per sample, while a mono sound file only has
one.

.. versionchanged:: 2.5.6 sndarray module is lazily loaded to avoid an expensive NumPy import when unnecessary
"""

import numpy
from pygame.mixer import Sound
from typing_extensions import deprecated  # added in 3.13

def array(sound: Sound) -> numpy.ndarray:
    """Copy Sound samples into an array.

    Creates a new array for the sound data and copies the samples. The array
    will always be in the format returned from ``pygame.mixer.get_init()``.
    """

def samples(sound: Sound) -> numpy.ndarray:
    """Reference Sound samples into an array.

    Creates a new array that directly references the samples in a Sound object.
    Modifying the array will change the Sound. The array will always be in the
    format returned from ``pygame.mixer.get_init()``.
    """

def make_sound(array: numpy.ndarray) -> Sound:
    """Convert an array into a Sound object.

    Create a new playable Sound object from an array. The mixer module must be
    initialized and the array format must be similar to the mixer audio format.
    """

@deprecated("Only numpy is supported")
def use_arraytype(arraytype: str) -> None:
    """Sets the array system to be used for sound arrays.

    DEPRECATED: Uses the requested array type for the module functions. The
    only supported arraytype is ``'numpy'``. Other values will raise ValueError.
    Using this function will raise a ``DeprecationWarning``.
    """

@deprecated("Only numpy is supported")
def get_arraytype() -> str:
    """Gets the currently active array type.

    DEPRECATED: Returns the currently active array type. This will be a value of the
    ``get_arraytypes()`` tuple and indicates which type of array module is used
    for the array creation. Using this function will raise a ``DeprecationWarning``.

    .. versionaddedold:: 1.8
    """

@deprecated("Only numpy is supported")
def get_arraytypes() -> tuple[str]:
    """Gets the array system types currently supported.

    DEPRECATED: Checks which array systems are available and returns them as a tuple of
    strings. The values of the tuple can be used directly in the
    :func:`pygame.sndarray.use_arraytype` method. Using this function will
    raise a ``DeprecationWarning``.

    .. versionaddedold:: 1.8
    """

# keep in sync with sndarray.py
__all__ = [
    "array",
    "samples",
    "make_sound",
    "use_arraytype",
    "get_arraytype",
    "get_arraytypes",
]
