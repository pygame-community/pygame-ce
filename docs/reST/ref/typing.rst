.. include:: common.txt

:mod:`pygame.typing`
====================

.. module:: pygame.typing
   :synopsis: pygame module providing common typehints

| :sl:`pygame module providing common typehints`

A lot of pygame functions and methods allow the user to provide different types
for the same value like colors or coordinates. This module exports the most common
type aliases for proper typehint annotations.

.. versionadded:: 2.5.1

   * ``pygame.typing.PathLike``: An object representing a file path

   * ``pygame.typing.FileLike``: An object representing a file

   * ``pygame.typing.SequenceLike``: A variant of the standard ``Sequence`` ABC
     only requiring ``__getitem__`` and ``__len__``

   * ``pygame.typing.Coordinate``: A sequence of two numbers (``pygame.Vector2`` included)

   * ``pygame.typing.IntCoordinate``: A sequence of strictly two integers

   * ``pygame.typing.RGBATuple``: A tuple of four integers in range 0-255
   
   * ``pygame.typing.ColorLike``: An object representing a color such as a mapped integer, 
     a string or a sequence of three or four integers in range 0-255 (``pygame.Color`` included),
     types supported by every function accepting a color argument

   * ``pygame.typing.RectLike``: An ibject representing a rect such as a sequence
     of numbers or coordinates (``pygame.Rect`` included) or an object with a rect attribute
     or a method returning a rect. This types are supported by every function accepting
     a rect as argument.


.. ## pygame.typing ##
