.. include:: common.txt

:mod:`pygame.geometry`
======================

.. module:: pygame.geometry
   :synopsis: pygame geometry module

   | :sl:`pygame module for the Circle, Rect, and Polygon objects`

.. currentmodule:: pygame

.. class:: Circle

   | :sl:`pygame object representing a circle`
   | :sg:`Circle(center, radius) -> Circle`
   | :sg:`Circle(x, y, radius) -> Circle`
   | :sg:`Circle(object) -> Circle`

   .. attribute:: x

         | :sl:`center x coordinate of the circle`
         | :sg:`x -> float`

         The `x` coordinate of the center of the circle.

         .. ## Circle.x ##

   .. attribute:: y

         | :sl:`center y coordinate of the circle`
         | :sg:`y -> float`

         The `y` coordinate of the center of the circle.

         .. ## Circle.y ##

   .. attribute:: r

         | :sl:`radius of the circle`
         | :sg:`r -> float`

         The `r` coordinate of the center of the circle. You cannot set the radius to a negative value.

         .. ## Circle.r ##

   .. method:: copy

         | :sl:`returns a copy of the circle`
         | :sg:`copy() -> Circle`

         The `copy` method returns a new `Circle` object having the same position and radius
         as the original `Circle`. The function takes no arguments.

         .. ## Circle.copy ##

   .. ## pygame.Circle ##