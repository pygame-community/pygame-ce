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

   The `Circle` class provides many useful methods for collision / transform and intersection.
   A `Circle` can be created from a combination of a pair of coordinates that represent
   the center of the circle and a radius. Circles can also be created from python objects that
   are already a `Circle` or have an attribute named "circle".

   Specifically, to construct a circle you can pass the x, y, and radius values as separate
   arguments or inside a sequence(list or tuple).

   Functions that require a `Circle` argument may also accept these values as Circles:

   ::

      ((x, y), radius)
      (x, y, radius)

   The `Circle` class has both virtual and non-virtual attributes. Non-virtual attributes
   are attributes that are stored in the `Circle` object itself. Virtual attributes are the
   result of calculations that utilize the Circle's non-virtual attributes.

   Here is the list of all the attributes and methods of the Circle class:

   **Circle Attributes**

   ----

   .. attribute:: x

         | :sl:`center x coordinate of the circle`
         | :sg:`x -> float`

         The `x` coordinate of the center of the circle. It can be reassigned to move the circle.
         Reassigning the `x` attribute will move the circle to the new `x` coordinate.
         The `y` and `r` attributes will not be affected.

         .. versionadded:: 2.4.0

         .. ## Circle.x ##

   .. attribute:: y

         | :sl:`center y coordinate of the circle`
         | :sg:`y -> float`

         The `y` coordinate of the center of the circle. It can be reassigned to move the circle.
         Reassigning the `y` attribute will move the circle to the new `y` coordinate.
         The `x` and `r` attributes will not be affected.

         .. versionadded:: 2.4.0

         .. ## Circle.y ##

   .. attribute:: r

         | :sl:`radius of the circle`
         | :sg:`r -> float`

         It is not possible to set the radius to a negative value. It can be reassigned.
         If reassigned it will only change the radius of the circle.
         The circle will not be moved from its original position.

         .. versionadded:: 2.4.0

         .. versionchanged:: 2.5.1 It is allowed to create degenerate circles with radius
            equal to ``0``. This also applies to virtual attributes.

         .. ## Circle.r ##

   .. attribute:: r_sqr

         | :sl:`radius of the circle squared`
         | :sg:`r_sqr -> float`

         It's equivalent to `r*r`. It can be reassigned. If reassigned, the radius
         of the circle will be changed to the square root of the new value.
         The circle will not be moved from its original position.

         .. versionadded:: 2.4.0

         .. ## Circle.r_sqr ##

   .. attribute:: center

         | :sl:`x and y coordinates of the center of the circle`
         | :sg:`center -> (float, float)`

         It's a tuple containing the `x` and `y` coordinates that represent the center
         of the circle. It can be reassigned. If reassigned, the circle will be moved
         to the new position. The radius will not be affected.

         .. versionadded:: 2.4.0

         .. ## Circle.center ##

   .. attribute:: diameter

         | :sl:`diameter of the circle`
         | :sg:`diameter -> float`

         It's calculated using the `d=2*r` formula. It can be reassigned. If reassigned
         the radius will be changed to half the diameter.
         The circle will not be moved from its original position.

         .. versionadded:: 2.4.0

         .. ## Circle.diameter ##

   .. attribute:: area

         | :sl:`area of the circle`
         | :sg:`area -> float`

         It's calculated using the `area=pi*r*r` formula. It can be reassigned.
         If reassigned the circle radius will be changed to produce a circle with matching
         area. The circle will not be moved from its original position.

         .. versionadded:: 2.4.0

         .. ## Circle.area ##

   .. attribute:: circumference

         | :sl:`circumference of the circle`
         | :sg:`circumference -> float`

         It's calculated using the `circumference=2*pi*r` formula. It can be reassigned.
         If reassigned the circle radius will be changed to produce a circle with matching
         circumference. The circle will not be moved from its original position.

         .. versionadded:: 2.4.0

         .. ## Circle.circumference ##

   **Circle Methods**

   ----

   .. method:: collidepoint

         | :sl:`test if a point is inside the circle`
         | :sg:`collidepoint((x, y), /) -> bool`
         | :sg:`collidepoint(x, y, /) -> bool`
         | :sg:`collidepoint(vector2, /) -> bool`

         The `collidepoint` method tests whether a given point is inside the `Circle`
         (including the edge of the `Circle`). It takes a tuple of (x, y) coordinates, two
         separate x and y coordinates, or a `Vector2` object as its argument, and returns
         `True` if the point is inside the `Circle`, `False` otherwise.

         .. versionadded:: 2.4.0

         .. ## Circle.collidepoint ##

   .. method:: collidecircle

         | :sl:`test if two circles collide`
         | :sg:`collidecircle(circle, /) -> bool`
         | :sg:`collidecircle(x, y, radius, /) -> bool`
         | :sg:`collidecircle((x, y), radius, /) -> bool`

         The `collidecircle` method tests whether two `Circle` objects overlap. It takes either
         a `Circle` object, a tuple of (x, y) coordinates and a radius, or separate x and y
         coordinates and a radius as its argument, and returns `True` if any portion of the two
         `Circle` objects overlap, `False` otherwise.

         .. note::
             If this method is called with a `Circle` object that is the same as the `Circle`
             it is called on, it will always return `True`.

         .. versionadded:: 2.4.0

         .. ## Circle.collidecircle ##

   .. method:: move

         | :sl:`moves the circle by a given amount`
         | :sg:`move((x, y), /) -> Circle`
         | :sg:`move(x, y, /) -> Circle`
         | :sg:`move(vector2, /) -> Circle`

         The `move` method allows you to create a new `Circle` object that is moved by a given
         offset from the original `Circle`. This is useful if you want to move a `Circle` without
         modifying the original. The move method takes either a tuple of (x, y) coordinates,
         two separate x and y coordinates, or a `Vector2` object as its argument, and returns
         a new `Circle` object with the updated position.

         .. note::
             This method is equivalent(behaviour wise) to the following code:

             .. code-block:: python

                 Circle((circle.x + x, circle.y + y), circle.r)

         .. versionadded:: 2.5.0

         .. ## Circle.move ##

   .. method:: move_ip

         | :sl:`moves the circle by a given amount, in place`
         | :sg:`move_ip((x, y), /) -> None`
         | :sg:`move_ip(x, y, /) -> None`
         | :sg:`move_ip(vector2, /) -> None`

         The `move_ip` method is similar to the move method, but it moves the `Circle` in place,
         modifying the original `Circle` object. This method takes the same types of arguments
         as move, and it always returns None.

         .. note::
             This method is equivalent(behaviour wise) to the following code:

             .. code-block:: python

                 circle.x += x
                 circle.y += y

         .. versionadded:: 2.5.0

         .. ## Circle.move_ip ##

   .. method:: colliderect

         | :sl:`checks if a rectangle intersects the circle`
         | :sg:`colliderect(rect, /) -> bool`
         | :sg:`colliderect((x, y, width, height), /) -> bool`
         | :sg:`colliderect(x, y, width, height, /) -> bool`
         | :sg:`colliderect((x, y), (width, height), /) -> bool`

         The `colliderect` method tests whether a given rectangle intersects the `Circle`. It
         takes either a `Rect` object, a tuple of (x, y, width, height) coordinates, or separate
         x, y coordinates and width, height as its argument. Returns `True` if any portion
         of the rectangle overlaps with the `Circle`, `False` otherwise.

         .. versionadded:: 2.4.0
         
         .. ## Circle.colliderect ##

   .. method:: collideswith

         | :sl:`check if a shape or point collides with the circle`
         | :sg:`collideswith(circle, /) -> bool`
         | :sg:`collideswith(rect, /) -> bool`
         | :sg:`collideswith((x, y), /) -> bool`
         | :sg:`collideswith(vector2, /) -> bool`

         The `collideswith` method checks if a shape or point overlaps with a `Circle` object.
         It takes a single argument which can be a `Circle`, `Rect`, `FRect`, or a point.
         It returns `True` if there's an overlap, and `False` otherwise.

         .. note::
             The shape argument must be an actual shape object (`Circle`, `Rect`, or `FRect`).
             You can't pass a tuple or list of coordinates representing the shape (except for a point),
             because the shape type can't be determined from the coordinates alone.

         .. versionadded:: 2.5.0

         .. ## Circle.collideswith ##

   .. method:: contains

         | :sl:`check if a shape or point is inside the circle`
         | :sg:`contains(circle, /) -> bool`
         | :sg:`contains(rect, /) -> bool`
         | :sg:`contains((x, y), /) -> bool`
         | :sg:`contains(vector2, /) -> bool`

         Checks whether a given shape or point is completely contained within the `Circle`.
         Takes a single argument which can be a `Circle`, `Rect`, `FRect`, or a point.
         Returns `True` if the shape or point is completely contained, and `False` otherwise.

         .. note::
             The shape argument must be an actual shape object (`Circle`, `Rect`, or `FRect`).
             You can't pass a tuple or list of coordinates representing the shape (except for a point),
             because the shape type can't be determined from the coordinates alone.

         .. versionadded:: 2.5.0

         .. ## Circle.contains ##

   .. method:: update

         | :sl:`updates the circle position and radius`
         | :sg:`update((x, y), radius, /) -> None`
         | :sg:`update(x, y, radius, /) -> None`

         The `update` method allows you to set the position and radius of a `Circle` object in
         place. This method takes either a tuple of (x, y) coordinates, two separate x and
         y coordinates, and a radius as its arguments, and it always returns `None`.

         .. note::
             This method is equivalent(behaviour wise) to the following code:

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

         Returns a new `Circle` that is rotated by the specified angle around a point.
         A positive angle rotates the circle clockwise, while a negative angle rotates it counter-clockwise. Angles should be specified in degrees.
         The rotation point can be a `tuple`, `list`, or `Vector2`.
         If no rotation point is given, the circle will be rotated around its center.

         .. versionadded:: 2.5.0

         .. ## Circle.rotate ##

   .. method:: rotate_ip

         | :sl:`rotates the circle in place`
         | :sg:`rotate_ip(angle, rotation_point=Circle.center, /) -> None`
         | :sg:`rotate_ip(angle, /) -> None`


         This method rotates the circle by a specified angle around a point.
         A positive angle rotates the circle clockwise, while a negative angle rotates it counter-clockwise. Angles should be specified in degrees.
         The rotation point can be a `tuple`, `list`, or `Vector2`.
         If no rotation point is given, the circle will be rotated around its center.

         .. versionadded:: 2.5.0

         .. ## Circle.rotate_ip ##

   .. method:: as_rect

         | :sl:`returns the smallest pygame.Rect object that contains the circle`
         | :sg:`as_rect() -> Rect`

         The `as_rect` method returns a `pygame.Rect` object that represents the smallest
         rectangle that completely contains the `Circle` object. This means that the `Rect`
         object returned by as_rect will have dimensions such that it completely encloses
         the `Circle`, with no part of the `Circle` extending outside of the `Rect`.

         .. note::
             This method is equivalent(behaviour wise) to the following code:

             .. code-block:: python

                 Rect(circle.x - circle.r, circle.y - circle.r, circle.r * 2, circle.r * 2)

         .. versionadded:: 2.5.0

         .. ## Circle.as_rect ##

   .. method:: as_frect

         | :sl:`returns the smallest pygame.FRect object that contains the circle`
         | :sg:`as_frect() -> FRect`

         The `as_frect` method returns a `pygame.FRect` object that represents the smallest
         rectangle that completely contains the `Circle` object. This means that the `FRect`
         object returned by as_rect will have dimensions such that it completely encloses
         the `Circle`, with no part of the `Circle` extending outside of the `FRect`.

         .. note::
             This method is equivalent(behaviour wise) to the following code:

             .. code-block:: python

                 FRect(circle.x - circle.r, circle.y - circle.r, circle.r * 2, circle.r * 2)

         .. versionadded:: 2.5.0

         .. ## Circle.as_frect ##

   .. method:: copy

         | :sl:`returns a copy of the circle`
         | :sg:`copy() -> Circle`

         The `copy` method returns a new `Circle` object having the same position and radius
         as the original `Circle` object. The function takes no arguments and returns the
         new `Circle` object.

         .. versionadded:: 2.4.0

         .. ## Circle.copy ##

   .. ## pygame.Circle ##