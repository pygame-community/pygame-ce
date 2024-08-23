.. include:: common.txt

:mod:`pygame.typing`
====================

.. module:: pygame.typing
   :synopsis: pygame module providing common typehints

| :sl:`pygame module providing common typehints`

.. versionadded:: 2.5.2

A lot of pygame functions and methods allow the user to provide different types
for the same value like colors or coordinates. This module exports the most common
type aliases for proper typehint annotations.

   .. data:: PathLike

      An object representing a file path, i.e.:

        * ``"my/string/path.txt"``
        * ``pathlib.Path("my/pathlib/path.txt")``
        * ``b"my/bytes/path.txt"``
        * Any object implementing the path protocol (with a ``__fspath__`` magic method)

   .. data:: FileLike

      An object representing a file. Same as :mod:`pygame.typing.PathLike` with
      the addition of file buffers (``IO`` of strings or bytes) such as the
      return value of ``open()``.

   .. data:: SequenceLike

      A variant of the standard ``Sequence`` ABC only requiring ``__getitem__``
      and ``__len__``. This includes custom sequences or builtin ones, i.e.:

        * ``"abcdefg"``
        * ``[a, b, c, d, ...]``
        * ``(a, b, c, d, ...)``

      Being a generic, subscribing it will signal further precision such as
      ``SequenceLike[str]`` or ``SequenceLike[float]``.
      
   .. data:: Coordinate

      A sequence of two numbers (floats or ints), i.e:

        * ``pygame.Vector2(a, b)`` 
        * ``[a, b]``
        * ``(a, b)``

   .. data:: IntCoordinate

      A sequence of strictly two integers such as ``[a, b]`` or ``(a, b)``.

   .. data:: RGBATuple

      A tuple of four integers ``(r, g, b, a)`` in range 0-255 such as ``(20, 255, 0, 100)``.

   .. data:: ColorLike

      An object representing a color such as a mapped integer, a string or
      a sequence of three or four integers in range 0-255, types supported by
      every function accepting a color argument. i.e.:

        * ``pygame.Color(ColorLike)``
        * ``(r, g, b)``
        * ``(r, g, b, a)``
        * ``[r, g, b, a]``
        * ``"green"``
        * ``0`` (mapped color)

   .. data:: RectLike
      
      An object representing a rect such as a sequence of numbers or coordinates
      or an object with a rect attribute or a method returning a rect. These types
      are supported by every function accepting a rect as argument. i.e.:

        * ``(x, y, w, h)``
        * ``(Coordinate, Coordinate)``
        * ``pygame.Rect(RectLike)``
        * Any object with a ``.rect`` attribute which is a ``RectLike`` or a function
          returning a ``RectLike``

.. ## pygame.typing ##
