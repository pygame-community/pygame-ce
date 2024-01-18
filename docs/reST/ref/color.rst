.. include:: common.txt

:mod:`pygame.Color`
===================

.. currentmodule:: pygame

.. class:: Color

   | :sl:`pygame object for color representations`
   | :sg:`Color(r, g, b) -> Color`
   | :sg:`Color(r, g, b, a=255) -> Color`
   | :sg:`Color(color_value) -> Color`

   The ``Color`` class represents ``RGBA`` color values using a value range of
   0 to 255 inclusive. It allows basic arithmetic operations — binary
   operations ``+``, ``-``, ``*``, ``//``, ``%``, and unary operation ``~`` — to
   create new colors, supports conversions to other color spaces such as ``HSV``
   or ``HSL`` and lets you adjust single color channels.
   Alpha defaults to 255 (fully opaque) when not given.
   The arithmetic operations and ``correct_gamma()`` method preserve subclasses.
   For the binary operators, the class of the returned color is that of the
   left hand color object of the operator.

   Color objects support swizzling for their ``RGBA`` attributes, which allows
   the creation of new color objects with the corresponding swizzled attributes
   as its ``RGBA`` attributes. For example, ``color.bgra`` provides a shortcut to
   doing ``Color(color.b, color.g, color.r, color.a)``. Swizzling with other than
   4 attributes will return a tuple consisting of the corresponding elements
   instead of a color object.

   Color objects support equality comparison with other color objects and 3 or
   4 element tuples of integers. There was a bug in pygame 1.8.1
   where the default alpha was 0, not 255 like previously.

   Color objects export the C level array interface. The interface exports a
   read-only one dimensional unsigned byte array of the same assigned length
   as the color. The new buffer interface is also exported, with the same
   characteristics as the array interface.

   The floor division, ``//``, and modulus, ``%``, operators do not raise
   an exception for division by zero. Instead, if a color, or alpha, channel
   in the right hand color is 0, then the result is 0. For example: ::

       # These expressions are True
       Color(255, 255, 255, 255) // Color(0, 64, 64, 64) == Color(0, 3, 3, 3)
       Color(255, 255, 255, 255) % Color(64, 64, 64, 0) == Color(63, 63, 63, 0)

   Use ``int(color)`` to return the immutable integer value of the color,
   usable as a ``dict`` key. This integer value differs from the mapped
   pixel values of :meth:`pygame.Surface.get_at_mapped`,
   :meth:`pygame.Surface.map_rgb` and :meth:`pygame.Surface.unmap_rgb`.
   It can be passed as a ``color_value`` argument to :class:`Color`
   (useful with sets).

   See :doc:`color_list` for samples of the available named colors.

   :param int r: red value in the range of 0 to 255 inclusive
   :param int g: green value in the range of 0 to 255 inclusive
   :param int b: blue value in the range of 0 to 255 inclusive
   :param int a: (optional) alpha value in the range of 0 to 255 inclusive,
      default is 255
   :param color_value: color value (see note below for the supported formats)

      .. note::
         Supported ``color_value`` formats:
            | - **Color object:** clones the given :class:`Color` object
            | - **Color name: str:** name of the color to use, e.g. ``'red'``
              (all the supported name strings can be found in the
               :doc:`color_list`, with sample swatches)
            | - **HTML color format str:** ``'#rrggbbaa'`` or ``'#rrggbb'``,
              where rr, gg, bb, and aa are 2-digit hex numbers in the range
              of 0 to 0xFF inclusive, the aa (alpha) value defaults to 0xFF
              if not provided
            | - **hex number str:** ``'0xrrggbbaa'`` or ``'0xrrggbb'``, where
              rr, gg, bb, and aa are 2-digit hex numbers in the range of 0x00
              to 0xFF inclusive, the aa (alpha) value defaults to 0xFF if not
              provided
            | - **int:** int value of the color to use, using hex numbers can
              make this parameter more readable, e.g. ``0xrrggbbaa``, where rr,
              gg, bb, and aa are 2-digit hex numbers in the range of 0x00 to
              0xFF inclusive, note that the aa (alpha) value is not optional for
              the int format and must be provided
            | - **tuple/list of int color values:** ``(R, G, B, A)`` or
              ``(R, G, B)``, where R, G, B, and A are int values in the range of
              0 to 255 inclusive, the A (alpha) value defaults to 255 if not
              provided

   :type color_value: Color or str or int or tuple(int, int, int, [int]) or
      list(int, int, int, [int])

   :returns: a newly created :class:`Color` object
   :rtype: Color

   .. versionchangedold:: 2.0.0
      Support for tuples, lists, and :class:`Color` objects when creating
      :class:`Color` objects.
   .. versionchangedold:: 1.9.2 Color objects export the C level array interface.
   .. versionchangedold:: 1.9.0 Color objects support 4-element tuples of integers.
   .. versionchangedold:: 1.8.1 New implementation of the class.

   .. attribute:: r

      | :sl:`Gets or sets the red value of the Color.`
      | :sg:`r -> int`

      The red value of the Color.

      .. ## Color.r ##

   .. attribute:: g

      | :sl:`Gets or sets the green value of the Color.`
      | :sg:`g -> int`

      The green value of the Color.

      .. ## Color.g ##

   .. attribute:: b

      | :sl:`Gets or sets the blue value of the Color.`
      | :sg:`b -> int`

      The blue value of the Color.

      .. ## Color.b ##

   .. attribute:: a

      | :sl:`Gets or sets the alpha value of the Color.`
      | :sg:`a -> int`

      The alpha value of the Color.

      .. ## Color.a ##

   .. attribute:: cmy

      | :sl:`Gets or sets the CMY representation of the Color.`
      | :sg:`cmy -> tuple`

      The ``CMY`` representation of the Color. The ``CMY`` components are in
      the ranges ``C`` = [0, 1], ``M`` = [0, 1], ``Y`` = [0, 1]. Note that this
      will not return the absolutely exact ``CMY`` values for the set ``RGB``
      values in all cases. Due to the ``RGB`` mapping from 0-255 and the
      ``CMY`` mapping from 0-1 rounding errors may cause the ``CMY`` values to
      differ slightly from what you might expect.

      .. ## Color.cmy ##

   .. attribute:: hsva

      | :sl:`Gets or sets the HSVA representation of the Color.`
      | :sg:`hsva -> tuple`

      The ``HSVA`` representation of the Color. The ``HSVA`` components are in
      the ranges ``H`` = [0, 360], ``S`` = [0, 100], ``V`` = [0, 100], A = [0,
      100]. Note that this will not return the absolutely exact ``HSV`` values
      for the set ``RGB`` values in all cases. Due to the ``RGB`` mapping from
      0-255 and the ``HSV`` mapping from 0-100 and 0-360 rounding errors may
      cause the ``HSV`` values to differ slightly from what you might expect.

      .. ## Color.hsva ##

   .. attribute:: hsla

      | :sl:`Gets or sets the HSLA representation of the Color.`
      | :sg:`hsla -> tuple`

      The ``HSLA`` representation of the Color. The ``HSLA`` components are in
      the ranges ``H`` = [0, 360], ``S`` = [0, 100], ``L`` = [0, 100], A = [0,
      100]. Note that this will not return the absolutely exact ``HSL`` values
      for the set ``RGB`` values in all cases. Due to the ``RGB`` mapping from
      0-255 and the ``HSL`` mapping from 0-100 and 0-360 rounding errors may
      cause the ``HSL`` values to differ slightly from what you might expect.

      .. ## Color.hsla ##

   .. attribute:: i1i2i3

      | :sl:`Gets or sets the I1I2I3 representation of the Color.`
      | :sg:`i1i2i3 -> tuple`

      The ``I1I2I3`` representation of the Color. The ``I1I2I3`` components are
      in the ranges ``I1`` = [0, 1], ``I2`` = [-0.5, 0.5], ``I3`` = [-0.5,
      0.5]. Note that this will not return the absolutely exact ``I1I2I3``
      values for the set ``RGB`` values in all cases. Due to the ``RGB``
      mapping from 0-255 and the ``I1I2I3`` mapping from 0-1 rounding errors
      may cause the ``I1I2I3`` values to differ slightly from what you might
      expect.

      .. ## Color.i1i2i3 ##
   
   .. classmethod:: from_cmy

      | :sl:`Returns a Color object from a CMY representation`
      | :sg:`from_cmy(object, /) -> Color`
      | :sg:`from_cmy(c, m, y, /) -> Color`

      Creates a Color object from the given CMY components. Refer to :attr:`Color.cmy`
      for more information.

      .. versionadded:: 2.3.1

      .. ## Color.from_cmy ##
   
   .. classmethod:: from_hsva

      | :sl:`Returns a Color object from an HSVA representation`
      | :sg:`from_hsva(object, /) -> Color`
      | :sg:`from_hsva(h, s, v, a, /) -> Color`

      Creates a Color object from the given HSVA components. Refer to :attr:`Color.hsva`
      for more information.

      .. versionadded:: 2.3.1

      .. ## Color.from_hsva ##
   
   .. classmethod:: from_hsla

      | :sl:`Returns a Color object from an HSLA representation`
      | :sg:`from_hsla(object, /) -> Color`
      | :sg:`from_hsla(h, s, l, a, /) -> Color`

      Creates a Color object from the given HSLA components. Refer to :attr:`Color.hsla`
      for more information.

      .. versionadded:: 2.3.1

      .. ## Color.from_hsla ##

   .. classmethod:: from_i1i2i3

      | :sl:`Returns a Color object from a I1I2I3 representation`
      | :sg:`from_i1i2i3(object, /) -> Color`
      | :sg:`from_i1i2i3(i1, i2, i3, /) -> Color`

      Creates a Color object from the given I1I2I3 components. Refer to :attr:`Color.i1i2i3`
      for more information.

      .. versionadded:: 2.3.1

      .. ## Color.from_i1i2i3 ##

   .. method:: normalize

      | :sl:`Returns the normalized RGBA values of the Color.`
      | :sg:`normalize() -> tuple`

      Returns the normalized ``RGBA`` values of the Color as floating point
      values.

      .. ## Color.normalize ##

   .. method:: correct_gamma

      | :sl:`Applies a certain gamma value to the Color.`
      | :sg:`correct_gamma(gamma, /) -> Color`

      Applies a certain gamma value to the Color and returns a new Color with
      the adjusted ``RGBA`` values.

      .. ## Color.correct_gamma ##

   .. method:: set_length

      | :sl:`Set the number of elements in the Color to 1,2,3, or 4.`
      | :sg:`set_length(len, /) -> None`

      DEPRECATED: You may unpack the values you need like so, 
      ``r, g, b, _ = pygame.Color(100, 100, 100)``
      If you only want r, g and b
      Or 
      ``r, g, *_ = pygame.Color(100, 100, 100)`` 
      if you only want r and g

      The default Color length is 4. Colors can have lengths 1,2,3 or 4. This
      is useful if you want to unpack to r,g,b and not r,g,b,a. If you want to
      get the length of a Color do ``len(acolor)``.

      .. deprecated:: 2.1.3
      .. versionaddedold:: 1.9.0

      .. ## Color.set_length ##

   .. method:: grayscale

      | :sl:`returns the grayscale of a Color`
      | :sg:`grayscale() -> Color`
      
      Returns a new Color object which represents the grayscaled version of self, using the luminosity formula, 
      which weights red, green, and blue according to their relative contribution to perceived brightness.

      .. versionadded:: 2.1.4

      .. ## Color.grayscale ##

   .. method:: lerp

      | :sl:`returns a linear interpolation to the given Color.`
      | :sg:`lerp(Color, float) -> Color`

      Returns a Color which is a linear interpolation between self and the
      given Color in RGBA space. The second parameter determines how far
      between self and other the result is going to be.
      It must be a value between 0 and 1 where 0 means self and 1 means
      other will be returned.

      .. versionaddedold:: 2.0.1

      .. ## Color.lerp ##

   .. method:: premul_alpha

      | :sl:`returns a Color where the r,g,b components have been multiplied by the alpha.`
      | :sg:`premul_alpha() -> Color`

      Returns a new Color where each of the red, green and blue colour
      channels have been multiplied by the alpha channel of the original
      color. The alpha channel remains unchanged.

      This is useful when working with the ``BLEND_PREMULTIPLIED`` blending mode
      flag for :meth:`pygame.Surface.blit()`, which assumes that all surfaces using
      it are using pre-multiplied alpha colors.

      .. versionaddedold:: 2.0.0

      .. ## Color.premul_alpha ##

   .. method:: update

      | :sl:`Sets the elements of the color`
      | :sg:`update(r, g, b, /) -> None`
      | :sg:`update(r, g, b, a=255, /) -> None`
      | :sg:`update(color_value, /) -> None`

      Sets the elements of the color. See parameters for :meth:`pygame.Color` for the
      parameters of this function. If the alpha value was not set it will not change.

      .. versionaddedold:: 2.0.1

      .. ## Color.update ##
   .. ## pygame.Color ##
