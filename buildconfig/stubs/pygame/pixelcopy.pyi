"""Pygame module for general pixel array copying.

The ``pygame.pixelcopy`` module contains functions for copying between
surfaces and objects exporting an array structure interface. It is a backend
for :mod:`pygame.surfarray`, adding NumPy support. But pixelcopy is more
general, and intended for direct use.

The array struct interface exposes an array's data in a standard way.
It was introduced in NumPy. In Python 2.7 and above it is replaced by the
new buffer protocol, though the buffer protocol is still a work in progress.
The array struct interface, on the other hand, is stable and works with earlier
Python versions. So for now the array struct interface is the predominate way
pygame handles array introspection.

For 2d arrays of integer pixel values, the values are mapped to the
pixel format of the related surface. To get the actual color of a pixel
value use :meth:`pygame.Surface.unmap_rgb`. 2d arrays can only be used
directly between surfaces having the same pixel layout.

New in pygame 1.9.2.
"""

from typing import Literal, TypeAlias

import numpy
from pygame.surface import Surface

_Kind: TypeAlias = Literal["P", "p", "R", "r", "G", "g", "B", "b", "A", "a", "C", "c"]

def surface_to_array(
    array: numpy.ndarray,
    surface: Surface,
    kind: _Kind = "P",
    opaque: int = 255,
    clear: int = 0,
) -> None:
    """Copy surface pixels to an array object.

    The surface_to_array function copies pixels from a Surface object
    to a 2D or 3D array. Depending on argument ``kind`` and the target array
    dimension, a copy may be raw pixel value, RGB, a color component slice,
    or colorkey alpha transparency value. Recognized ``kind`` values are the
    single character codes 'P', 'R', 'G', 'B', 'A', and 'C'. Kind codes are case
    insensitive, so 'p' is equivalent to 'P'. The first two dimensions
    of the target must be the surface size (w, h).

    The default 'P' kind code does a direct raw integer pixel (mapped) value
    copy to a 2D array and a 'RGB' pixel component (unmapped) copy to a 3D array
    having shape (w, h, 3). For an 8 bit colormap surface this means the
    table index is copied to a 2D array, not the table value itself. A 2D
    array's item size must be at least as large as the surface's pixel
    byte size. The item size of a 3D array must be at least one byte.

    For the 'R', 'G', 'B', and 'A' copy kinds a single color component
    of the unmapped surface pixels are copied to the target 2D array.
    For kind 'A' and surfaces with source alpha (the surface was created with
    the SRCALPHA flag), has a colorkey
    (set with :meth:`Surface.set_colorkey() <pygame.Surface.set_colorkey>`),
    or has a blanket alpha
    (set with :meth:`Surface.set_alpha() <pygame.Surface.set_alpha>`)
    then the alpha values are those expected for a SDL surface.
    If a surface has no explicit alpha value, then the target array
    is filled with the value of the optional ``opaque`` surface_to_array
    argument (default 255: not transparent).

    Copy kind 'C' is a special case for alpha copy of a source surface
    with colorkey. Unlike the 'A' color component copy, the ``clear``
    argument value is used for colorkey matches, ``opaque`` otherwise.
    By default, a match has alpha 0 (totally transparent), while everything
    else is alpha 255 (totally opaque). It is a more general implementation
    of :meth:`pygame.surfarray.array_colorkey`.

    Specific to surface_to_array, a ValueError is raised for target arrays
    with incorrect shape or item size. A TypeError is raised for an incorrect
    kind code. Surface specific problems, such as locking, raise a pygame.error.
    """

def array_to_surface(surface: Surface, array: numpy.ndarray, /) -> None:
    """Copy an array object to a surface.

    See :func:`pygame.surfarray.blit_array`.
    """

def map_array(
    array1: numpy.ndarray, array2: numpy.ndarray, surface: Surface, /
) -> None:
    """Copy an array to another array, using surface format.

    Map an array of color element values - (w, h, ..., 3) - to an array of
    pixels - (w, h) according to the format of <surface>.
    """

def make_surface(array: numpy.ndarray, /) -> Surface:
    """Copy an array to a new surface.

    Create a new Surface that best resembles the data and format of the array.
    The array can be 2D or 3D with any sized integer values.
    """
