.. include:: common.txt

:mod:`pygame.Rect`
==================

.. currentmodule:: pygame

.. class:: Rect
   
   | :sl:`Pygame object for storing rectangular coordinates.`
   | :sg:`Rect(left, top, width, height, /) -> Rect`
   | :sg:`Rect((left, top), (width, height), /) -> Rect`
   | :sg:`Rect(object, /) -> Rect`
   | :sg:`Rect() -> Rect`
   | :sg:`FRect(left, top, width, height, /) -> FRect`
   | :sg:`FRect((left, top), (width, height), /) -> FRect`
   | :sg:`FRect(object, /) -> FRect`
   | :sg:`FRect() -> FRect`

   .. versionadded:: 2.2
      Added ``FRect`` class that is functionally identical to ``Rect`` but uses
      floats instead of integers, enabling fractional precision and avoiding
      truncation error while being interchangeable with standard Rects.

   Pygame uses Rect objects to store and manipulate rectangular areas. A Rect
   can be created from a combination of left, top, width, and height values.
   Rects can also be created from python objects that are already a Rect or
   have an attribute named "rect".

   Any pygame function that requires a Rect argument also accepts any of these
   values to construct a Rect. This makes it easier to create Rects on the fly
   as arguments to functions.

   If no arguments are given, a zero Rect will be created (x=0, y=0, w=0, h=0).
   This will only work when using the Rect/FRect class and not with functions
   that require a Rect argument.

   The Rect functions that change the position or size of a Rect return a new
   copy of the Rect with the affected changes. The original Rect is not
   modified. Some methods have an alternate "in-place" version that returns
   None but affects the original Rect. These "in-place" methods are denoted
   with the "ip" suffix.

   The Rect object has several virtual attributes which can be used to move and
   align the Rect:

   ::

       x,y
       top, left, bottom, right
       topleft, bottomleft, topright, bottomright
       midtop, midleft, midbottom, midright
       center, centerx, centery
       size, width, height, relcenter
       w,h

   All of these attributes can be assigned to:

   ::

       rect1.right = 10
       rect2.center = (20,30)

   Assigning to size, width, height, or relcenter changes the dimensions of the rectangle;
   all other assignments move the rectangle without resizing it. Notice that
   some attributes are integers and others are pairs of integers.

   If a Rect has a nonzero width or height, it will return ``True`` for a
   nonzero test. Some methods return a Rect with 0 size to represent an invalid
   rectangle. A Rect with a 0 size will not collide when using collision
   detection methods (e.g. :meth:`collidepoint`, :meth:`colliderect`, etc.).

   The coordinates for Rect objects are all integers. The size values can be
   programmed to have negative values, but these are considered illegal Rects
   for most operations.

   There are several collision tests between other rectangles. Most python
   containers can be searched for collisions against a single Rect.

   The area covered by a Rect does not include the right- and bottom-most edge
   of pixels. If one Rect's bottom border is another Rect's top border (i.e.,
   rect1.bottom=rect2.top), the two meet exactly on the screen but do not
   overlap, and ``rect1.colliderect(rect2)`` returns false.

   The Rect object is also iterable:

   ::

      r = Rect(0, 1, 2, 3)
      x, y, w, h = r

   .. versionaddedold:: 1.9.2
      The Rect class can be subclassed. Methods such as ``copy()`` and ``move()``
      will recognize this and return instances of the subclass.
      However, the subclass's ``__init__()`` method is not called,
      and ``__new__()`` is assumed to take no arguments. So these methods should be
      overridden if any extra attributes need to be copied.

   .. versionadded:: 2.5.6
      ``relcenter`` added to Rect / FRect. This will return a tuple containing half
      the Rect's size; the center relative to the topleft of the Rect.
      Setting it to a ``Point`` will modify the size of the rect to 2 times
      the ``Point`` given. Below you can find a code example of how it should work:

      .. code-block:: python

         >>> my_rect = pygame.Rect(0, 0, 2, 2)
         >>> my_rect.relcenter
         (1, 1)
         >>> my_rect.relcenter = (128, 128)
         >>> my_rect.size
         (256, 256)

      Beware of non-integer relative centers! For Rects (but not FRects), ``relcenter``
      will truncate the numbers in the returned tuple.

   .. autopgmethod:: copy

   .. autopgmethod:: move

   .. autopgmethod:: move_ip

   .. autopgmethod:: move_to

   .. autopgmethod:: inflate

   .. autopgmethod:: inflate_ip

   .. autopgmethod:: scale_by

   .. autopgmethod:: scale_by_ip

   .. autopgmethod:: update

   .. autopgmethod:: clamp

   .. autopgmethod:: clamp_ip

   .. autopgmethod:: clip

   .. autopgmethod:: clipline

   .. autopgmethod:: union

   .. autopgmethod:: union_ip

   .. autopgmethod:: unionall

   .. autopgmethod:: unionall_ip

   .. autopgmethod:: fit

   .. autopgmethod:: normalize

   .. autopgmethod:: contains

   .. autopgmethod:: collidepoint

   .. autopgmethod:: colliderect

   .. autopgmethod:: collidelist

   .. autopgmethod:: collidelistall

   .. autopgmethod:: collideobjects

   .. autopgmethod:: collideobjectsall

   .. autopgmethod:: collidedict

   .. autopgmethod:: collidedictall
