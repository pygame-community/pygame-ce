.. include:: common.txt

:mod:`pygame.typing`
====================

.. module:: pygame.typing
   :synopsis: pygame module providing common typehints

| :sl:`pygame module providing common typehints`

.. versionadded:: 2.5.2

A lot of pygame functions and methods allow the user to provide different types
for the same value like colors or points. This module exports the most common
type aliases for proper typehint annotations.

   .. data:: FileLike

      An object representing a file. This includes both path-like
      objects and file-like objects, i.e.:

        * ``"my/string/path.txt"``
        * ``open("my/file/path.txt")``
        * ``pathlib.Path("my/pathlib/path.txt")``
        * ``io.BytesIO(b"my data: \x00\x01")``
        * ``b"my/bytes/path.txt"``
        * Any object implementing the path protocol or file protocol.

   .. data:: SequenceLike

      A variant of the standard ``Sequence`` ABC only requiring ``__getitem__``
      and ``__len__``. This includes custom sequences or builtin ones, i.e.:

        * ``"abcdefg"``
        * ``[a, b, c, d, ...]``
        * ``(a, b, c, d, ...)``

      Being a generic, subscribing it will signal further precision such as
      ``SequenceLike[str]`` or ``SequenceLike[float]``.

   .. data:: Point

      A sequence of two numbers (floats or ints), i.e:

        * ``pygame.Vector2(a, b)``
        * ``[a, b]``
        * ``(a, b)``

   .. data:: IntPoint

      A sequence of strictly two integers such as ``[a, b]`` or ``(a, b)``.

   .. data:: ColorLike

      An object representing a color such as a mapped integer, a string or
      a sequence of three or four integers in range 0-255, types supported by
      every function accepting a color argument. i.e.:

        * ``pygame.Color(ColorLike)``
        * ``(r, g, b)``
        * ``(r, g, b, a)``
        * ``[r, g, b, a]``
        * ``"green"`` (:doc:`color_list`)
        * ``"#rrggbbaa"``
        * ``0`` (mapped color)

   .. data:: RectLike

      An object representing a rect such as a sequence of numbers or points
      or an object with a rect attribute or a method returning a rect. These types
      are supported by every function accepting a rect as argument. i.e.:

        * ``(x, y, w, h)``
        * ``(Point, Point)``
        * ``pygame.Rect(RectLike)``
        * Any object with a ``.rect`` attribute which is a ``RectLike`` or a function
          returning a ``RectLike``

.. ## pygame.typing ##
