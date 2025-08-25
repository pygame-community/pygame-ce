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

   The `Circle` class provides many useful methods for collision testing, transformation and intersection.
   A `Circle` can be created from a combination of a pair of coordinates that represent
   the center of the circle and a radius. Circles can also be created from python objects that
   are already a `Circle` (effectively copying the circle) or have an attribute named "circle".

   Specifically, to construct a circle you can pass the x, y, and radius values as separate
   arguments or inside a sequence(list or tuple).

   Functions that require a `Circle` argument may also accept these values as Circles:

   ::

      ((x, y), radius)
      (x, y, radius)
      (vector2, radius)

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

         Represents the size of the circle. It can't be negative. Reassigning it scales the circle.

         .. versionadded:: 2.4.0

         .. versionchanged:: 2.5.1 It is now allowed to create degenerate circles with :math:`r = 0`.

         .. ## Circle.r ##

   .. attribute:: r_sqr

         | :sl:`radius of the circle squared`
         | :sg:`r_sqr -> float`

         It's equivalent to :math:`r^2`. It can't be negative. Reassigning it changes the radius to :math:`r = \sqrt{r_{sqr}}`.

         .. versionadded:: 2.4.0

         .. ## Circle.r_sqr ##

   .. attribute:: center

         | :sl:`x and y coordinates of the center of the circle`
         | :sg:`center -> (float, float)`

         A tuple containing the circle's `x` and `y` coordinates representing its center.
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

   .. attribute:: top

         | :sl:`top coordinate of the circle`
         | :sg:`top -> (float, float)`

         A tuple containing the `x` and `y` coordinates that represent the top
         of the circle.
         Reassigning it moves the circle to the new position. The radius will not be affected.

         .. versionadded:: 2.5.2

         .. ## Circle.top ##

   .. attribute:: bottom

         | :sl:`bottom coordinate of the circle`
         | :sg:`bottom -> (float, float)`

         A tuple containing the `x` and `y` coordinates that represent the bottom
         of the circle.
         Reassigning it moves the circle to the new position. The radius will not be affected.

         .. versionadded:: 2.5.2

         .. ## Circle.bottom ##

   .. attribute:: left

         | :sl:`left coordinate of the circle`
         | :sg:`left -> (float, float)`

         A tuple containing the `x` and `y` coordinates that represent the left
         of the circle.
         Reassigning it moves the circle to the new position. The radius will not be affected.

         .. versionadded:: 2.5.2

         .. ## Circle.left ##

   .. attribute:: right

         | :sl:`right coordinate of the circle`
         | :sg:`right -> (float, float)`

         A tuple containing the `x` and `y` coordinates that represent the right
         of the circle.
         Reassigning it moves the circle to the new position. The radius will not be affected.

         .. versionadded:: 2.5.2

         .. ## Circle.right ##

   **Circle Methods**

   ----

   .. method:: collidepoint

         | :sl:`tests if a point is inside the circle`
         | :sg:`collidepoint((x, y), /) -> bool`
         | :sg:`collidepoint(x, y, /) -> bool`
         | :sg:`collidepoint(vector2, /) -> bool`

         Returns `True` if the given point is inside this `Circle` (edge included), `False` otherwise.
         It takes a tuple of (x, y) coordinates, two separate x and y coordinates, or a `Vector2`
         object as its argument.

         .. versionadded:: 2.4.0

         .. ## Circle.collidepoint ##

   .. method:: collidecircle

         | :sl:`tests if a circle collides with this circle`
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

         | :sl:`tests if a rectangle collides with this circle`
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

   .. method:: collidelist

         | :sl:`test if a list of objects collide with the circle`
         | :sg:`collidelist(colliders) -> int`

         The `collidelist` method tests whether a given list of shapes or points collides
         (overlaps) with this `Circle` object. The function takes in a single argument, which
         must be a list of `Circle`, `Rect`, `FRect`, or a point. The function returns the index
         of the first shape or point in the list that collides with the `Circle` object, or
         -1 if there is no collision.

         .. note::
             The shapes must be actual shape objects, such as `Circle`, `Rect` or `FRect`
             instances. It is not possible to pass a tuple or list of coordinates representing
             the shape as an argument (except for a point), because the shape type can't be
             determined from the coordinates alone.

         .. versionadded:: 2.5.2

         .. ## Circle.collidelist ##

   .. method:: collidelistall

         | :sl:`test if all objects in a list collide with the circle`
         | :sg:`collidelistall(colliders) -> list`

         The `collidelistall` method tests whether a given list of shapes or points collides
         (overlaps) with this `Circle` object. The function takes in a single argument, which
         must be a list of `Circle`, `Rect`, `FRect`, or a point. The function returns a list
         containing the indices of all the shapes or points in the list that collide with
         the `Circle` object, or an empty list if there is no collision.

         .. note::
             The shapes must be actual shape objects, such as `Circle`, `Rect` or `FRect`
             instances. It is not possible to pass a tuple or list of coordinates representing
             the shape as an argument (except for a point), because the shape type can't be
             determined from the coordinates alone.

         .. versionadded:: 2.5.2

         .. ## Circle.collidelistall ##

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

         Returns a copy of this `Circle` moved by the given amounts.
         Takes either a tuple of (x, y) coordinates, two separate x and y coordinates,
         or a `Vector2` object as its argument.

         This method is equivalent to the following code:

         .. code-block:: python

             Circle((circle.x + x, circle.y + y), circle.r)

         .. versionadded:: 2.5.0

         .. ## Circle.move ##

   .. method:: move_ip

         | :sl:`moves the circle by a given amount, in place`
         | :sg:`move_ip((x, y), /) -> None`
         | :sg:`move_ip(x, y, /) -> None`
         | :sg:`move_ip(vector2, /) -> None`

         Moves this `Circle` in place by the given amounts.
         Takes the same types of arguments as :meth:`move` and it always returns `None`.

         This method is equivalent to the following code:

         .. code-block:: python

             circle.x += x
             circle.y += y

         .. versionadded:: 2.5.0

         .. ## Circle.move_ip ##

   .. method:: intersect

         | :sl:`finds intersections between the circle and a shape`
         | :sg:`intersect(circle, /) -> list`

        Finds and returns a list of intersection points between the circle and another shape.
        The other shape must be a `Circle` object.
        If the circle does not intersect or has infinite intersections, an empty list is returned.

        .. note::
            The shape argument must be an instance of the `Circle` class.
            Passing a tuple or list of coordinates representing the shape is not supported,
            as the type of shape cannot be determined from coordinates alone.

         .. versionadded:: 2.5.2

         .. ## Circle.intersect ##

   .. method:: update

         | :sl:`updates the circle position and radius`
         | :sg:`update((x, y), radius, /) -> None`
         | :sg:`update(x, y, radius, /) -> None`
         | :sg:`update(vector2, radius, /) -> None`

         Sets the position and radius of this `Circle` to the provided values.
         It always returns `None`.

         This method is equivalent to the following code:

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
         The rotation point is optional and defaults to the circle's center.

         .. versionadded:: 2.5.0

         .. ## Circle.rotate ##

   .. method:: rotate_ip

         | :sl:`rotates the circle in place`
         | :sg:`rotate_ip(angle, rotation_point=Circle.center, /) -> None`
         | :sg:`rotate_ip(angle, /) -> None`

         Rotates the circle by a specified angle (in degrees) around a point.
         Positive angles rotate the circle clockwise, counter-clockwise otherwise.
         The rotation point is optional and defaults to the circle's center.

         .. versionadded:: 2.5.0

         .. ## Circle.rotate_ip ##

   .. method:: as_rect

         | :sl:`returns the smallest Rect containing the circle`
         | :sg:`as_rect() -> Rect`

         Returns the smallest `pygame.Rect` object containing this `Circle`.

         This method is equivalent to the following code:

         .. code-block:: python

             Rect(circle.x - circle.r, circle.y - circle.r, circle.r * 2, circle.r * 2)

         .. versionadded:: 2.5.0

         .. ## Circle.as_rect ##

   .. method:: as_frect

         | :sl:`returns the smallest FRect containing the circle`
         | :sg:`as_frect() -> FRect`

         Returns the smallest `pygame.FRect` object containing this `Circle`.

         This method is equivalent to the following code:

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


.. class:: Line

   | :sl:`pygame object for representing a line`
   | :sg:`Line((ax, ay), (bx, by)) -> Line`
   | :sg:`Line(ax, ay, bx, by) -> Line`

   .. versionadded:: 2.5.2

   The `Line` class provides many useful methods for collision testing, transformation and intersection.
   A `Line` can be created from a combination of two pairs of coordinates that represent the start and end points.
   Lines can also be created from python objects that are already a `Line` (effectively copying the line) or have an attribute named "line".

   Specifically, to construct a `Line` you can pass the ax, ay, bx, and by values as separate
   arguments or inside a sequence(list or tuple).

   As a special case you can also pass in `pygame.Rect` / `pygame.FRect`, in which case the
   line will be created with (x, y, width, height) as the start and end points.

   You can create lines with the same start and end points, but beware that some methods may
   not work as expected or error out.

   Functions that require a `Line` argument may also accept these values as Lines:

   ::

      ((ax, ay), (bx, by))
      (ax, ay, bx, by)
      (vector2, vector2)

   The `Line` class only stores the ax, ay, bx, and by attributes, everything else is calculated
   on the fly based on them.

   **Line Attributes**

   ----

   .. attribute:: ax

         | :sl:`x coordinate of the start point of the line`
         | :sg:`ax -> float`

         The horizontal coordinate of the start point of the line. Reassigning it moves the line.

         .. versionadded:: 2.5.2

         .. ## Line.ax ##

   .. attribute:: ay

         | :sl:`y coordinate of the start point of the line`
         | :sg:`ay -> float`

         The vertical coordinate of the start point of the line. Reassigning it moves the line.

         .. versionadded:: 2.5.2

         .. ## Line.ay ##

   .. attribute:: bx

         | :sl:`x coordinate of the end point of the line`
         | :sg:`bx -> float`

         The horizontal coordinate of the end point of the line. Reassigning it moves the line.

         .. versionadded:: 2.5.2

         .. ## Line.bx ##

   .. attribute:: by

         | :sl:`y coordinate of the end point of the line`
         | :sg:`by -> float`

         The vertical coordinate of the end point of the line. Reassigning it moves the line.

         .. versionadded:: 2.5.2

         .. ## Line.by ##

   .. attribute:: a

         | :sl:`the first point of the line`
         | :sg:`a -> (float, float)`

         A tuple containing the `ax` and `ay` attributes representing the line's first point.
         It can be reassigned to move the `Line`. If reassigned the `ax` and `ay` attributes
         will be changed to produce a `Line` with matching first point position.
         The `bx` and `by` attributes will not be affected.

         .. versionadded:: 2.5.2

         .. ## Line.a ##

   .. attribute:: b

         | :sl:`the second point of the line`
         | :sg:`b -> (float, float)`

         A tuple containing `bx` and `by` attributes representing the line's second point.
         It can be reassigned to move the `Line`. If reassigned the `bx` and `by` attributes
         will be changed to produce a `Line` with matching second point position.
         The `ax` and `ay` attributes will not be affected.

         .. versionadded:: 2.5.2

         .. ## Line.b ##

   .. attribute:: length

         | :sl:`the length of the line`
         | :sg:`length -> float`

         The length of the line. Calculated using the `sqrt((bx-ax)**2 + (by-ay)**2)` formula.
         This attribute is read-only, it cannot be reassigned. To change the line's length
         use the `scale` method or change its `a` or `b` attributes.

         .. versionadded:: 2.5.3

         .. ## Line.length ##

   **Line Methods**

   ----

   .. method:: copy

         | :sl:`copies the line`
         | :sg:`copy() -> Line`

         Returns a copy of this `Line`.

         .. versionadded:: 2.5.2

         .. ## Line.copy ##

   .. method:: move

         | :sl:`moves the line by a given amount`
         | :sg:`move((x, y)) -> Line`
         | :sg:`move(x, y) -> Line`

         Returns a new `Line` that is moved by the given offset. The original `Line` is
         not modified.

         This method is equivalent to the following code:

         .. code-block:: python

             Line(line.ax + x, line.ay + y, line.bx + x, line.by + y)

         .. versionadded:: 2.5.3

      .. ## Line.move ##

   .. method:: move_ip

         | :sl:`moves the line by a given amount`
         | :sg:`move_ip((x, y)) -> None`
         | :sg:`move_ip(x, y) -> None`

         Moves the `Line` by the given offset. The original `Line` is modified. Always returns
         `None`.

         This method is equivalent to the following code:

         .. code-block:: python

             line.ax += x
             line.ay += y
             line.bx += x
             line.by += y

         .. versionadded:: 2.5.3

      .. ## Line.move_ip ##

   .. method:: update

         | :sl:`updates the line's attributes`
         | :sg:`update((ax, ay), (bx, by)) -> None`
         | :sg:`update(ax, ay, bx, by) -> None`
         | :sg:`update(line) -> None`

         Updates the `Line`'s attributes. The original `Line` is modified. Always returns `None`.

         This method is equivalent to the following code:

         .. code-block:: python

             line.ax = ax
             line.ay = ay
             line.bx = bx
             line.by = by

         .. versionadded:: 2.5.3

      .. ## Line.update ##

   .. method:: scale

         | :sl:`scales the line by the given factor from the given origin`
         | :sg:`scale(factor, origin) -> Line`
         | :sg:`scale(factor_and_origin) -> Line`

         Returns a new `Line` which is scaled by the given factor from the specified origin with 0.0 being
         the starting point, 0.5 being the center and 1.0 being the end point.
         The original `Line` is not modified.

         .. versionadded:: 2.5.3

      .. ## Line.scale ##

   .. method:: scale_ip

         | :sl:`scales the line by the given factor from the given origin in place`
         | :sg:`scale_ip(factor, origin) -> None`
         | :sg:`scale_ip(factor_and_origin) -> None`

         Scales the `Line` by the given factor from the specified origin with 0.0 being
         the starting point, 0.5 being the center and 1.0 being the end point.
         The original `Line` is modified.
         Always returns `None`.

         .. versionadded:: 2.5.3

      .. ## Line.scale_ip ##

   .. method:: flip_ab

         | :sl:`flips the line a and b points`
         | :sg:`flip_ab() -> Line`

         Returns a new `Line` that has the `a` and `b` points flipped.
         The original `Line` is not modified.

         .. versionadded:: 2.5.3

      .. ## Line.flip_ab ##

   .. method:: flip_ab_ip

         | :sl:`flips the line a and b points, in place`
         | :sg:`flip_ab_ip() -> None`

         Flips the `Line`'s `a` and `b` points. The original `Line` is modified.
         Always returns `None`.

         .. versionadded:: 2.5.3

      .. ## Line.flip_ab_ip ##
