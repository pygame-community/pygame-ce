.. include:: common.txt

:mod:`pygame.geometry`
======================

.. module:: pygame.geometry
   :synopsis: pygame geometry module

   .. warning::
      **Experimental Module**

      **This module is a work in progress. Refrain from relying on any features provided by
      this module, as they are subject to change or removal without prior notice.**

   .. versionadded:: 2.4.0

   | :sl:`pygame module for the Circle, Line, and Polygon objects`

.. currentmodule:: pygame

.. class:: Circle

   | :sl:`pygame object for representing a circle`
   | :sg:`Circle((x, y), radius) -> Circle`
   | :sg:`Circle(x, y, radius) -> Circle`

   The `Circle` class provides many useful methods for collision, transformation, and intersection.
   A `Circle` can be created from a combination of a pair of coordinates that represent
   the center of the circle and a radius. Circles can also be created from python objects that
   are already a `Circle` (effectively copying the circle) or have an attribute named "circle".

   Specifically, to construct a circle you can pass the x, y, and radius values as separate
   arguments or inside a sequence(list or tuple).

   Functions that require a `Circle` argument may also accept these values as Circles:

   ::

      ((x, y), radius)
      (x, y, radius)

   The `Circle` class only stores the x, y and r attributes, everything else is calculated
   on the fly based on them.

   **Circle Attributes**

   ----

   .. attribute:: x

         | :sl:`center x coordinate of the circle`
         | :sg:`x -> float`

         The horizontal coordinate of the center of the circle. Reassigning it moves the circle.

         .. versionadded:: 2.4.0

         .. ## Circle.x ##

   .. attribute:: y

         | :sl:`center y coordinate of the circle`
         | :sg:`y -> float`

         The vertical coordinate of the center of the circle. Reassigning it moves the circle.

         .. versionadded:: 2.4.0

         .. ## Circle.y ##

   .. attribute:: r

         | :sl:`radius of the circle`
         | :sg:`r -> float`

         Represents how big the circle is. It can't be negative. Reassigning it scales the circle.

         .. versionadded:: 2.4.0

         .. versionchanged:: 2.5.1 It is allowed to create degenerate circles with radius
            equal to ``0``. This also applies to virtual attributes.

         .. ## Circle.r ##

   .. attribute:: r_sqr

         | :sl:`radius of the circle squared`
         | :sg:`r_sqr -> float`

         It's equivalent to :math:`r^2`. Reassigning it changes the radius to :math:`r = \sqrt{r_{sqr}}`.

         .. versionadded:: 2.4.0

         .. ## Circle.r_sqr ##

   .. attribute:: center

         | :sl:`x and y coordinates of the center of the circle`
         | :sg:`center -> (float, float)`

         It's a tuple containing the circle's `x` and `y` coordinates representing its center.
         Reassigning it moves the circle to the new position.

         .. versionadded:: 2.4.0

         .. ## Circle.center ##

   .. attribute:: diameter

         | :sl:`diameter of the circle`
         | :sg:`diameter -> float`

         It's equivalent to :math:`2 \cdot r`. It can't be negative. Reassigning it
         changes the radius to :math:`r = \frac{d}{2}`.

         .. versionadded:: 2.4.0

         .. ## Circle.diameter ##

   .. attribute:: area

         | :sl:`area of the circle`
         | :sg:`area -> float`

         It's equivalent to :math:`\pi \cdot r^2`. It can't be negative. Reassigning it
         changes the radius to :math:`r = \sqrt{\frac{area}{\pi}}` producing a circle with matching area.

         .. versionadded:: 2.4.0

         .. ## Circle.area ##

   .. attribute:: circumference

         | :sl:`circumference of the circle`
         | :sg:`circumference -> float`

         It's equivalent to :math:`2 \cdot \pi \cdot r`. It can't be negative. Reassigning it
         changes the radius to :math:`r = \frac{circumference}{2\pi}` producing a circle with
         matching circumference.

         .. versionadded:: 2.4.0

         .. ## Circle.circumference ##

   **Circle Methods**

   ----

   .. method:: collidepoint

         | :sl:`test if a point is inside the circle`
         | :sg:`collidepoint((x, y), /) -> bool`
         | :sg:`collidepoint(x, y, /) -> bool`
         | :sg:`collidepoint(vector2, /) -> bool`

         Returns `True` if the given point is inside this `Circle` (edge included), `False` otherwise.
         It takes a tuple of (x, y) coordinates, two separate x and y coordinates, or a `Vector2`
         object as its argument.

         .. versionadded:: 2.4.0

         .. ## Circle.collidepoint ##

   .. method:: collidecircle

         | :sl:`test if a circle collides with this circle`
         | :sg:`collidecircle(circle, /) -> bool`
         | :sg:`collidecircle(x, y, radius, /) -> bool`
         | :sg:`collidecircle((x, y), radius, /) -> bool`
         | :sg:`collidecircle(vector2, radius, /) -> bool`

         Returns `True` if the given circle intersects with this `Circle`, `False` otherwise.
         It takes either a `Circle` object, a tuple of (x, y) coordinates and a radius, or separate x and y
         coordinates and a radius as its argument.

         .. note::
             Calling this method with this circle as the argument will always return `True`.

         .. versionadded:: 2.4.0

         .. ## Circle.collidecircle ##

   .. method:: colliderect

         | :sl:`test if a rectangle collides with this circle`
         | :sg:`colliderect(rect, /) -> bool`
         | :sg:`colliderect((x, y, width, height), /) -> bool`
         | :sg:`colliderect(x, y, width, height, /) -> bool`
         | :sg:`colliderect((x, y), (width, height), /) -> bool`
         | :sg:`colliderect(vector2, (width, height), /) -> bool`

         Returns `True` if the given rectangle intersects with this `Circle`, `False` otherwise.
         Takes either a `Rect` object, a tuple of (x, y, width, height) coordinates, or separate
         x, y coordinates and width, height as its argument.

         .. versionadded:: 2.4.0
         
         .. ## Circle.colliderect ##

   .. method:: collideswith

         | :sl:`tests if a shape or point collides with this circle`
         | :sg:`collideswith(circle, /) -> bool`
         | :sg:`collideswith(rect, /) -> bool`
         | :sg:`collideswith((x, y), /) -> bool`
         | :sg:`collideswith(vector2, /) -> bool`

         Returns `True` if the given shape or point intersects with this `Circle`, `False` otherwise.
         The shape can be a `Circle`, `Rect`, `FRect`.

         .. note::
             The shape argument must be an actual shape object (`Circle`, `Rect`, or `FRect`).
             You can't pass a tuple or list of coordinates representing the shape (except for a point),
             because the shape type can't be determined from the coordinates alone.

         .. versionadded:: 2.5.0

         .. ## Circle.collideswith ##

   .. method:: contains

         | :sl:`tests if a shape or point is inside the circle`
         | :sg:`contains(circle, /) -> bool`
         | :sg:`contains(rect, /) -> bool`
         | :sg:`contains((x, y), /) -> bool`
         | :sg:`contains(vector2, /) -> bool`

         Returns `True` if the shape or point is completely contained within this `Circle`, `False` otherwise.
         The shape can be a `Circle`, `Rect`, `FRect`.

         .. note::
             The shape argument must be an actual shape object (`Circle`, `Rect`, or `FRect`).
             You can't pass a tuple or list of coordinates representing the shape (except for a point),
             because the shape type can't be determined from the coordinates alone.

         .. versionadded:: 2.5.0

         .. ## Circle.contains ##

   .. method:: move

         | :sl:`moves the circle by a given amount`
         | :sg:`move((x, y), /) -> Circle`
         | :sg:`move(x, y, /) -> Circle`
         | :sg:`move(vector2, /) -> Circle`

         Returns a copy of this `Circle` that is moved by the given amount.
         Takes either a tuple of (x, y) coordinates, two separate x and y coordinates,
         or a `Vector2` object as its argument.

         .. note::
             This method is equivalent (behaviour wise) to the following code:

             .. code-block:: python

                 Circle((circle.x + x, circle.y + y), circle.r)

         .. versionadded:: 2.5.0

         .. ## Circle.move ##

   .. method:: move_ip

         | :sl:`moves the circle by a given amount, in place`
         | :sg:`move_ip((x, y), /) -> None`
         | :sg:`move_ip(x, y, /) -> None`
         | :sg:`move_ip(vector2, /) -> None`

         Moves this `Circle` in place by the given amount.
         Takes the same types of arguments as move, and it always returns `None`.

         .. note::
             This method is equivalent (behaviour wise) to the following code:

             .. code-block:: python

                 circle.x += x
                 circle.y += y

         .. versionadded:: 2.5.0

         .. ## Circle.move_ip ##

   .. method:: update

         | :sl:`updates the circle position and radius`
         | :sg:`update((x, y), radius, /) -> None`
         | :sg:`update(x, y, radius, /) -> None`
         | :sg:`update(vector2, radius, /) -> None`

         Sets the position and radius of this `Circle` to the provided values.
         It always returns `None`.

         .. note::
             This method is equivalent (behaviour wise) to the following code:

             .. code-block:: python

                 circle.x = x
                 circle.y = y
                 circle.r = radius

         .. versionadded:: 2.4.0

         .. ## Circle.update ##

   .. method:: rotate

         | :sl:`rotates the circle`
         | :sg:`rotate(angle, rotation_point=Circle.center, /) -> Circle`
         | :sg:`rotate(angle, /) -> Circle`

         Returns a copy of this `Circle` rotated by the specified angle (in degrees) around a point.
         Positive angles rotate the circle clockwise, counter-clockwise otherwise.
         The rotation point is optional and must be a valid 2D coordinate. If not provided,
         the circle will be rotated around its center.

         .. versionadded:: 2.5.0

         .. ## Circle.rotate ##

   .. method:: rotate_ip

         | :sl:`rotates the circle in place`
         | :sg:`rotate_ip(angle, rotation_point=Circle.center, /) -> None`
         | :sg:`rotate_ip(angle, /) -> None`


         Rotates the circle by a specified angle (in degrees) around a point.
         Positive angles rotate the circle clockwise, counter-clockwise otherwise.
         The rotation point is optional and must be a valid 2D coordinate. If not provided,
         the circle will be rotated around its center.

         .. versionadded:: 2.5.0

         .. ## Circle.rotate_ip ##

   .. method:: as_rect

         | :sl:`returns the smallest Rect containing the circle`
         | :sg:`as_rect() -> Rect`

         Returns the smallest `pygame.Rect` object containing this `Circle`.

         .. note::
             This method is equivalent (behaviour wise) to the following code:

             .. code-block:: python

                 Rect(circle.x - circle.r, circle.y - circle.r, circle.r * 2, circle.r * 2)

         .. versionadded:: 2.5.0

         .. ## Circle.as_rect ##

   .. method:: as_frect

         | :sl:`returns the smallest FRect containing the circle`
         | :sg:`as_frect() -> FRect`

         Returns the smallest `pygame.FRect` object containing this `Circle`.

         .. note::
             This method is equivalent (behaviour wise) to the following code:

             .. code-block:: python

                 FRect(circle.x - circle.r, circle.y - circle.r, circle.r * 2, circle.r * 2)

         .. versionadded:: 2.5.0

         .. ## Circle.as_frect ##

   .. method:: copy

         | :sl:`copies the circle`
         | :sg:`copy() -> Circle`

         Returns a copy of this `Circle`.

         .. versionadded:: 2.4.0

         .. ## Circle.copy ##

   .. ## pygame.Circle ##