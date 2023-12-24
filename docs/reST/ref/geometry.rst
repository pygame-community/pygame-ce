.. include:: common.txt

:mod:`pygame.geometry`
======================

.. module:: pygame.geometry
   :synopsis: pygame geometry module

   .. warning::
      **Experimental Module**

      **This module is a work in progress. Refrain from relying on any features provided by
      this module, as they are subject to change or removal without prior notice.**

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

   It is important to note that you cannot create degenerate circles, which are circles with
   a radius of 0 or less. If you try to create such a circle, the `Circle` object will not be
   created and an error will be raised. This is because a circle with a radius of 0 or
   less is not a valid geometric object.

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

         .. ## Circle.x ##

   .. attribute:: y

         | :sl:`center y coordinate of the circle`
         | :sg:`y -> float`

         The `y` coordinate of the center of the circle. It can be reassigned to move the circle.
         Reassigning the `y` attribute will move the circle to the new `y` coordinate.
         The `x` and `r` attributes will not be affected.

         .. ## Circle.y ##

   .. attribute:: r

         | :sl:`radius of the circle`
         | :sg:`r -> float`

         It is not possible to set the radius to a negative value. It can be reassigned.
         If reassigned it will only change the radius of the circle.
         The circle will not be moved from its original position.

         .. ## Circle.r ##

   .. attribute:: r_sqr

         | :sl:`radius of the circle squared`
         | :sg:`r_sqr -> float`

         It's equivalent to `r*r`. It can be reassigned. If reassigned, the radius
         of the circle will be changed to the square root of the new value.
         The circle will not be moved from its original position.

         .. ## Circle.r_sqr ##

   .. attribute:: center

         | :sl:`x and y coordinates of the center of the circle`
         | :sg:`center -> (float, float)`

         It's a tuple containing the `x` and `y` coordinates that represent the center
         of the circle. It can be reassigned. If reassigned, the circle will be moved
         to the new position. The radius will not be affected.

         .. ## Circle.center ##

   .. attribute:: diameter

         | :sl:`diameter of the circle`
         | :sg:`diameter -> float`

         It's calculated using the `d=2*r` formula. It can be reassigned. If reassigned
         the radius will be changed to half the diameter.
         The circle will not be moved from its original position.

         .. ## Circle.diameter ##

   .. attribute:: area

         | :sl:`area of the circle`
         | :sg:`area -> float`

         It's calculated using the `area=pi*r*r` formula. It can be reassigned.
         If reassigned the circle radius will be changed to produce a circle with matching
         area. The circle will not be moved from its original position.

         .. ## Circle.area ##

   .. attribute:: circumference

         | :sl:`circumference of the circle`
         | :sg:`circumference -> float`

         It's calculated using the `circumference=2*pi*r` formula. It can be reassigned.
         If reassigned the circle radius will be changed to produce a circle with matching
         circumference. The circle will not be moved from its original position.

         .. ## Circle.circumference ##

   **Circle Methods**

   ----

   .. method:: collidepoint

         | :sl:`test if a point is inside the circle`
         | :sg:`collidepoint((x, y)) -> bool`
         | :sg:`collidepoint(x, y) -> bool`
         | :sg:`collidepoint(Vector2) -> bool`

         The `collidepoint` method tests whether a given point is inside the `Circle`
         (including the edge of the `Circle`). It takes a tuple of (x, y) coordinates, two
         separate x and y coordinates, or a `Vector2` object as its argument, and returns
         `True` if the point is inside the `Circle`, `False` otherwise.

         .. ## Circle.collidepoint ##

   .. method:: collidecircle

         | :sl:`test if two circles collide`
         | :sg:`collidecircle(Circle) -> bool`
         | :sg:`collidecircle(x, y, radius) -> bool`
         | :sg:`collidecircle((x, y), radius) -> bool`

         The `collidecircle` method tests whether two `Circle` objects overlap. It takes either
         a `Circle` object, a tuple of (x, y) coordinates and a radius, or separate x and y
         coordinates and a radius as its argument, and returns `True` if any portion of the two
         `Circle` objects overlap, `False` otherwise.

         .. note::
             If this method is called with a `Circle` object that is the same as the `Circle`
             it is called on, it will always return `True`.

         .. ## Circle.collidecircle ##

   .. method:: colliderect

         | :sl:`checks if a rectangle intersects the circle`
         | :sg:`colliderect(Rect) -> bool`
         | :sg:`colliderect((x, y, width, height)) -> bool`
         | :sg:`colliderect(x, y, width, height) -> bool`
         | :sg:`colliderect((x, y), (width, height)) -> bool`

         The `colliderect` method tests whether a given rectangle intersects the `Circle`. It
         takes either a `Rect` object, a tuple of (x, y, width, height) coordinates, or separate
         x, y coordinates and width, height as its argument. Returns `True` if any portion
         of the rectangle overlaps with the `Circle`, `False` otherwise.
         
         .. ## Circle.colliderect ##

   .. method:: update

         | :sl:`updates the circle position and radius`
         | :sg:`update((x, y), radius) -> None`
         | :sg:`update(x, y, radius) -> None`

         The `update` method allows you to set the position and radius of a `Circle` object in
         place. This method takes either a tuple of (x, y) coordinates, two separate x and
         y coordinates, and a radius as its arguments, and it always returns `None`.

         .. note::
             This method is equivalent(behaviour wise) to the following code:

             .. code-block:: python

                 circle.x = x
                 circle.y = y
                 circle.r = radius

         .. ## Circle.update ##

   .. method:: copy

         | :sl:`returns a copy of the circle`
         | :sg:`copy() -> Circle`

         The `copy` method returns a new `Circle` object having the same position and radius
         as the original `Circle` object. The function takes no arguments and returns the
         new `Circle` object.

         .. ## Circle.copy ##

   .. ## pygame.Circle ##