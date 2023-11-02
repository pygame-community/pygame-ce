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

   .. method:: copy

         | :sl:`returns a copy of the circle`
         | :sg:`copy() -> Circle`

         The `copy` method returns a new `Circle` object having the same position and radius
         as the original `Circle` object. The function takes no arguments and returns the
         new `Circle` object.

         .. ## Circle.copy ##

   .. ## pygame.Circle ##