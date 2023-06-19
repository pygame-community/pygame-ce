.. include:: common.txt

:mod:`pygame.Surface`
=====================

.. currentmodule:: pygame

.. class:: Surface

   | :sl:`pygame object for representing images`
   | :sg:`Surface((width, height), flags=0, depth=0, masks=None) -> Surface`
   | :sg:`Surface((width, height), flags=0, Surface) -> Surface`

   A pygame Surface is used to represent any image. The Surface has a fixed
   resolution and pixel format. Surfaces with 8-bit pixels use a color palette
   to map to 24-bit color.

   Call :meth:`pygame.Surface()` to create a new image object. The Surface will
   be cleared to all black. The only required arguments are the sizes. With no
   additional arguments, the Surface will be created in a format that best
   matches the display Surface.

   The pixel format can be controlled by passing the bit depth or an existing
   Surface. The flags argument is a bitmask of additional features for the
   surface. You can pass any combination of these flags:

   ::

     HWSURFACE    (obsolete in pygame 2) creates the image in video memory
     SRCALPHA     the pixel format will include a per-pixel alpha

   Both flags are only a request, and may not be possible for all displays and
   formats.

   Advance users can combine a set of bitmasks with a depth value. The masks
   are a set of 4 integers representing which bits in a pixel will represent
   each color. Normal Surfaces should not require the masks argument.

   Surfaces can have many extra attributes like alpha planes, colorkeys, source
   rectangle clipping. These functions mainly effect how the Surface is blitted
   to other Surfaces. The blit routines will attempt to use hardware
   acceleration when possible, otherwise they will use highly optimized
   software blitting methods.

   There are three types of transparency supported in pygame: colorkeys,
   surface alphas, and pixel alphas. Surface alphas can be mixed with
   colorkeys, but an image with per pixel alphas cannot use the other modes.
   Colorkey transparency makes a single color value transparent. Any pixels
   matching the colorkey will not be drawn. The surface alpha value is a single
   value that changes the transparency for the entire image. A surface alpha of
   255 is opaque, and a value of 0 is completely transparent.

   Per pixel alphas are different because they store a transparency value for
   every pixel. This allows for the most precise transparency effects, but it
   also the slowest. Per pixel alphas cannot be mixed with surface alpha and
   colorkeys.

   There is support for pixel access for the Surfaces. Pixel access on hardware
   surfaces is slow and not recommended. Pixels can be accessed using the
   :meth:`get_at()` and :meth:`set_at()` functions. These methods are fine for
   simple access, but will be considerably slow when doing of pixel work with
   them. If you plan on doing a lot of pixel level work, it is recommended to
   use a :class:`pygame.PixelArray`, which gives an array like view of the
   surface. For involved mathematical manipulations try the
   :mod:`pygame.surfarray` module (It's quite quick, but requires NumPy.)

   Any functions that directly access a surface's pixel data will need that
   surface to be lock()'ed. These functions can :meth:`lock()` and
   :meth:`unlock()` the surfaces themselves without assistance. But, if a
   function will be called many times, there will be a lot of overhead for
   multiple locking and unlocking of the surface. It is best to lock the
   surface manually before making the function call many times, and then
   unlocking when you are finished. All functions that need a locked surface
   will say so in their docs. Remember to leave the Surface locked only while
   necessary.

   Surface pixels are stored internally as a single number that has all the
   colors encoded into it. Use the :meth:`map_rgb()` and
   :meth:`unmap_rgb()` to convert between individual red, green, and blue
   values into a packed integer for that Surface.

   Surfaces can also reference sections of other Surfaces. These are created
   with the :meth:`subsurface()` method. Any change to either Surface will
   effect the other.

   Each Surface contains a clipping area. By default the clip area covers the
   entire Surface. If it is changed, all drawing operations will only effect
   the smaller area.

   .. method:: blit

      | :sl:`draw one image onto another`
      | :sg:`blit(source, dest, area=None, special_flags=0) -> Rect`

      Draws a Surface onto this Surface. The placement of the ``source`` surface on this surface
      can be specified by passing either a coordinate (x, y) or a Rect as the ``dest``
      parameter. The ``dest`` parameter denotes the upper left corner from where the blit operation
      will commence. In the case of a Rect, its top-left corner will be used.

      If you want to draw only a specific part of the source surface, you can pass a smaller
      rectangle as the ``area`` parameter representing that area. It is optional and defaults
      to ``None``, in which case the whole source surface will be drawn.

      The ``special_flags`` parameter can be used to control how the colors of the source
      surface are combined with the colors of this surface. It is optional and defaults to `0`,
      meaning a standard opaque blit will be performed (an alpha blit if the source surface
      has pixel or global alphas) if no flags are passed. See the **Special Flags** section
      below for a list of possible values.

      The function returns a rectangle representing the area of this surface that
      was affected by the blit operation, excluding any pixels outside this surface
      or its clipping area.

      Special Flags
      --------------

      The following blending flags affect how the colors are blended between the two surfaces:

      - Blending without Alpha Channel (RGB):
          - ``BLEND_ADD`` / ``BLEND_RGB_ADD``: Adds colors, excluding alpha.
          - ``BLEND_SUB`` / ``BLEND_RGB_SUB``: Subtracts colors, excluding alpha.
          - ``BLEND_MULT`` / ``BLEND_RGB_MULT``: Multiplies colors, excluding alpha.
          - ``BLEND_MIN`` / ``BLEND_RGB_MIN``: Takes the minimum value of each color component, excluding alpha.
          - ``BLEND_MAX`` / ``BLEND_RGB_MAX``: Takes the maximum value of each color component, excluding alpha.

      - Blending with Alpha Channel (RGBA):
          - ``BLEND_RGBA_ADD``: Adds colors, including alpha.
          - ``BLEND_RGBA_SUB``: Subtracts colors, including alpha.
          - ``BLEND_RGBA_MULT``: Multiplies colors, including alpha.
          - ``BLEND_RGBA_MIN``: Takes the minimum value of each color component, including alpha.
          - ``BLEND_RGBA_MAX``: Takes the maximum value of each color component, including alpha.

      - Special Alpha blending flags:
          - ``BLEND_PREMULTIPLIED``:
                Uses premultiplied alpha blending for faster and accurate results when
                the alpha channel is already multiplied into the color channels of the images.
                You should only use this blend mode if you previously premultiplied the source
                surface with :meth:`premul_alpha()`.
          - ``BLEND_ALPHA_SDL2``:
                Uses the SDL2 blitter for alpha blending, which may give slightly different
                results compared to the default blitter used in Pygame 1. This algorithm uses
                different approximations for alpha blending and supports Run-Length Encoding
                (RLE) on alpha-blended surfaces.

      Notes
      --------------

      .. note:: The size of the destination rectangle does not effect the blit.

      .. note:: When using the ``area`` parameter as a rectangle with negative positions, the
                resulting blit position will be different from the values passed. Specifically,
                the negative values of the rectangle will be subtracted from the corresponding
                ``dest`` coordinates. For example, if the original ``dest`` coordinates are
                (15, 15) and the rectangle defined by the ``area`` is (-5, -5, 10, 10), the final
                blit position will be (20, 20).

      .. note:: When blitting to an 8-bit surface, any transparency in the source surface will be ignored.

      .. note:: If you perform a self-blit (blitting to the same surface) with colorkey or alpha
                transparency, the resulting colors may appear slightly different compared to
                copying to a different surface.

      .. note:: The blit will be ignored if the source surface is completely outside the
                destination surface's clipping area. If the source surface is partially
                inside/outside the destination surface, only the overlapping area will be blitted.

      .. ## Surface.blit ##

   .. method:: blits

      | :sl:`draw many images onto another`
      | :sg:`blits(blit_sequence=((source, dest), ...), doreturn=True) -> [Rect, ...] or None`
      | :sg:`blits(((source, dest, area), ...)) -> [Rect, ...]`
      | :sg:`blits(((source, dest, area, special_flags), ...)) -> [Rect, ...]`

      The ``blits`` method efficiently draws a sequence of surfaces onto this ``Surface``.

      **Parameters**

          ``blit_sequence``
                A sequence that contains each surface to be drawn along with its associated blit
                arguments. See the **Sequence Item Formats** section below for the possible formats.

          ``doreturn`` (optional)
                The ``doreturn`` parameter controls the return value. When set to ``True``, it returns
                a list of rectangles representing the changed areas. When set to ``False``, returns
                ``None``.

      **Return**

          A list of rectangles or ``None``.

      **Sequence Item Formats**

          ``(source, dest)``
            - ``source``: Surface object to be drawn.
            - ``dest``: Position where the source Surface should be blitted.

          ``(source, dest, area)``
            - ``area``: (optional) Specific area of the source Surface to be drawn.

          ``(source, dest, area, special_flags)``
            - ``special_flags``: (optional) Controls the blending mode for drawing colors.

      **Notes**

          - ``blits`` is an advanced method. It is recommended to read the documentation
            of :meth:`blit` first.

          - To draw a ``Surface`` with a special flag, you must specify an area as well, e.g.,
            ``(source, dest, None, special_flags)``.

          - Prefer using :meth:`blits` over :meth:`blit` when drawing a multiple images
            for better performance. Use :meth:`blit` if you need to draw a single image.

          - For drawing a sequence of (source, dest) pairs with whole source Surface
            and a singular special_flag, use the :meth:`fblits()` method.

      .. versionaddedold:: 1.9.4

      .. ## Surface.blits ##

   .. method:: fblits

      | :sl:`draw many surfaces onto the calling surface at their corresponding location and the same special_flags`
      | :sg:`fblits(blit_sequence=((source, dest), ...), special_flags=0) -> None`

      This method takes a sequence of tuples (source, dest) as input, where source is a Surface
      object and dest is its destination position on this Surface. It draws each source Surface
      fully (meaning that unlike `blit()` you cannot pass an "area" parameter to represent
      a smaller portion of the source Surface to draw) on this Surface with the same blending
      mode specified by special_flags. The sequence must have at least one (source, dest) pair.

      :param blit_sequence: a sequence of (source, dest)
      :param special_flags: the flag(s) representing the blend mode used for each surface

      :returns: ``None``

      .. note:: This method only accepts a sequence of (source, dest) pairs and a single
                special_flags value that's applied to all surfaces drawn. This allows faster
                iteration over the sequence and better performance over `blits()`. Further
                optimizations are applied if blit_sequence is a list or a tuple (using one
                of them is recommended).

      .. versionadded:: 2.1.4

      .. ## Surface.fblits ##

   .. method:: convert

      | :sl:`change the pixel format of an image`
      | :sg:`convert(Surface=None) -> Surface`
      | :sg:`convert(depth, flags=0) -> Surface`
      | :sg:`convert(masks, flags=0) -> Surface`

      Creates a new copy of the Surface with the pixel format changed. The new
      pixel format can be determined from another existing Surface. Otherwise
      depth, flags, and masks arguments can be used, similar to the
      :meth:`pygame.Surface()` call.

      If no arguments are passed the new Surface will have the same pixel
      format as the display Surface. This is always the fastest format for
      blitting. It is a good idea to convert all Surfaces before they are
      blitted many times.

      The converted Surface will have no pixel alphas. They will be stripped if
      the original had them. See :meth:`convert_alpha()` for preserving or
      creating per-pixel alphas.

      The new copy will have the same class as the copied surface. This lets
      as Surface subclass inherit this method without the need to override,
      unless subclass specific instance attributes also need copying.

      .. ## Surface.convert ##

   .. method:: convert_alpha

      | :sl:`change the pixel format of an image including per pixel alphas`
      | :sg:`convert_alpha() -> Surface`

      Creates a new copy of the surface with the desired pixel format. The new
      surface will be in a format suited for quick blitting to the display surface
      with per pixel alpha.

      Unlike the :meth:`convert()` method, the pixel format for the new
      image will not be exactly the same as the display surface, but it will
      be optimized for fast alpha blitting to it.

      As with :meth:`convert()` the returned surface has the same class as
      the converted surface.

      .. versionchanged:: 2.4.0 'Surface' argument deprecated.

      .. ## Surface.convert_alpha ##

   .. method:: copy

      | :sl:`create a new copy of a Surface`
      | :sg:`copy() -> Surface`

      Makes a duplicate copy of a Surface. The new surface will have the same
      pixel formats, color palettes, transparency settings, and class as the
      original. If a Surface subclass also needs to copy any instance specific
      attributes then it should override ``copy()``. Shallow copy and deepcopy
      are supported, Surface implements __copy__ and __deepcopy__ respectively.

      .. versionadded:: 2.3.1
         Added support for deepcopy by implementing __deepcopy__, calls copy() internally.

      .. ## Surface.copy ##

   .. method:: fill

      | :sl:`fill Surface with a solid color`
      | :sg:`fill(color, rect=None, special_flags=0) -> Rect`

      Fill the Surface with a solid color. If no rect argument is given the
      entire Surface will be filled. The rect argument will limit the fill to a
      specific area. The fill will also be contained by the Surface clip area.

      The color argument can be an ``RGB`` sequence, an ``RGBA`` sequence,
      a string (for :doc:`color_list`), or a mapped color index. If using ``RGBA``,
      the Alpha (A part of ``RGBA``) is ignored unless the surface uses per pixel
      alpha (Surface has the ``SRCALPHA`` flag).

      .. versionaddedold:: 1.8
         Optional ``special_flags``: ``BLEND_ADD``, ``BLEND_SUB``,
         ``BLEND_MULT``, ``BLEND_MIN``, ``BLEND_MAX``.

      .. versionaddedold:: 1.8.1
         Optional ``special_flags``: ``BLEND_RGBA_ADD``, ``BLEND_RGBA_SUB``,
         ``BLEND_RGBA_MULT``, ``BLEND_RGBA_MIN``, ``BLEND_RGBA_MAX``
         ``BLEND_RGB_ADD``, ``BLEND_RGB_SUB``, ``BLEND_RGB_MULT``,
         ``BLEND_RGB_MIN``, ``BLEND_RGB_MAX``.

      This will return the affected Surface area.

      .. ## Surface.fill ##

   .. method:: scroll

      | :sl:`Shift the surface image in place`
      | :sg:`scroll(dx=0, dy=0) -> None`

      Move the image by dx pixels right and dy pixels down. dx and dy may be
      negative for left and up scrolls respectively. Areas of the surface that
      are not overwritten retain their original pixel values. Scrolling is
      contained by the Surface clip area. It is safe to have dx and dy values
      that exceed the surface size.

      .. versionaddedold:: 1.9

      .. ## Surface.scroll ##

   .. method:: set_colorkey

      | :sl:`Set the transparent colorkey`
      | :sg:`set_colorkey(color, flags=0) -> None`
      | :sg:`set_colorkey(None) -> None`

      Set the current color key for the Surface. When blitting this Surface
      onto a destination, any pixels that have the same color as the colorkey
      will be transparent. The color can be an ``RGB`` color, a string
      (for :doc:`color_list`), or a mapped color integer. If ``None`` is passed,
      the colorkey will be unset.

      The colorkey will be ignored if the Surface is formatted to use per pixel
      alpha values. The colorkey can be mixed with the full Surface alpha
      value.

      The optional flags argument can be set to ``pygame.RLEACCEL`` to provide
      better performance on non accelerated displays. An ``RLEACCEL`` Surface
      will be slower to modify, but quicker to blit as a source.

      .. ## Surface.set_colorkey ##

   .. method:: get_colorkey

      | :sl:`Get the current transparent colorkey`
      | :sg:`get_colorkey() -> RGB or None`

      Return the current colorkey value for the Surface. If the colorkey is not
      set then ``None`` is returned.

      .. ## Surface.get_colorkey ##

   .. method:: set_alpha

      | :sl:`set the alpha value for the full Surface image`
      | :sg:`set_alpha(value, flags=0) -> None`
      | :sg:`set_alpha(None) -> None`

      Set the current alpha value for the Surface. When blitting this Surface
      onto a destination, the pixels will be drawn slightly transparent. The
      alpha value is an integer from 0 to 255, 0 is fully transparent and 255
      is fully opaque. If ``None`` is passed for the alpha value, then alpha
      blending will be disabled, including per-pixel alpha.

      This value is different than the per pixel Surface alpha. For a surface
      with per pixel alpha, blanket alpha is ignored and ``None`` is returned.

      .. versionchangedold:: 2.0 per-surface alpha can be combined with per-pixel
                          alpha.

      The optional flags argument can be set to ``pygame.RLEACCEL`` to provide
      better performance on non accelerated displays. An ``RLEACCEL`` Surface
      will be slower to modify, but quicker to blit as a source.

      .. ## Surface.set_alpha ##

   .. method:: get_alpha

      | :sl:`get the current Surface transparency value`
      | :sg:`get_alpha() -> int_value`

      Return the current alpha value for the Surface.

      .. ## Surface.get_alpha ##

   .. method:: lock

      | :sl:`lock the Surface memory for pixel access`
      | :sg:`lock() -> None`

      Lock the pixel data of a Surface for access. On accelerated Surfaces, the
      pixel data may be stored in volatile video memory or nonlinear compressed
      forms. When a Surface is locked the pixel memory becomes available to
      access by regular software. Code that reads or writes pixel values will
      need the Surface to be locked.

      Surfaces should not remain locked for more than necessary. A locked
      Surface can often not be displayed or managed by pygame.

      Not all Surfaces require locking. The :meth:`mustlock()` method can
      determine if it is actually required. There is no performance penalty for
      locking and unlocking a Surface that does not need it.

      All pygame functions will automatically lock and unlock the Surface data
      as needed. If a section of code is going to make calls that will
      repeatedly lock and unlock the Surface many times, it can be helpful to
      wrap the block inside a lock and unlock pair.

      It is safe to nest locking and unlocking calls. The surface will only be
      unlocked after the final lock is released.

      .. ## Surface.lock ##

   .. method:: unlock

      | :sl:`unlock the Surface memory from pixel access`
      | :sg:`unlock() -> None`

      Unlock the Surface pixel data after it has been locked. The unlocked
      Surface can once again be drawn and managed by pygame. See the
      :meth:`lock()` documentation for more details.

      All pygame functions will automatically lock and unlock the Surface data
      as needed. If a section of code is going to make calls that will
      repeatedly lock and unlock the Surface many times, it can be helpful to
      wrap the block inside a lock and unlock pair.

      It is safe to nest locking and unlocking calls. The surface will only be
      unlocked after the final lock is released.

      .. ## Surface.unlock ##

   .. method:: mustlock

      | :sl:`test if the Surface requires locking`
      | :sg:`mustlock() -> bool`

      Returns ``True`` if the Surface is required to be locked to access pixel
      data. Usually pure software Surfaces do not require locking. This method
      is rarely needed, since it is safe and quickest to just lock all Surfaces
      as needed.

      All pygame functions will automatically lock and unlock the Surface data
      as needed. If a section of code is going to make calls that will
      repeatedly lock and unlock the Surface many times, it can be helpful to
      wrap the block inside a lock and unlock pair.

      .. ## Surface.mustlock ##

   .. method:: get_locked

      | :sl:`test if the Surface is current locked`
      | :sg:`get_locked() -> bool`

      Returns ``True`` when the Surface is locked. It doesn't matter how many
      times the Surface is locked.

      .. ## Surface.get_locked ##

   .. method:: get_locks

      | :sl:`Gets the locks for the Surface`
      | :sg:`get_locks() -> tuple`

      Returns the currently existing locks for the Surface.

      .. ## Surface.get_locks ##

   .. method:: get_at

      | :sl:`get the color value at a single pixel`
      | :sg:`get_at((x, y)) -> Color`

      Return a copy of the ``RGBA`` Color value at the given pixel. If the
      Surface has no per pixel alpha, then the alpha value will always be 255
      (opaque). If the pixel position is outside the area of the Surface an
      ``IndexError`` exception will be raised.

      Getting and setting pixels one at a time is generally too slow to be used
      in a game or realtime situation. It is better to use methods which
      operate on many pixels at a time like with the blit, fill and draw
      methods - or by using :mod:`pygame.surfarray`/:mod:`pygame.PixelArray`.

      This function will temporarily lock and unlock the Surface as needed.
      
      .. versionchanged:: 2.3.1 can now also accept both float coordinates and Vector2s for pixels.
      
         Returning a Color instead of tuple. Use ``tuple(surf.get_at((x,y)))``
         if you want a tuple, and not a Color. This should only matter if
         you want to use the color as a key in a dict.
      
      .. versionaddedold:: 1.9
      
      .. ## Surface.get_at ##

   .. method:: set_at

      | :sl:`set the color value for a single pixel`
      | :sg:`set_at((x, y), Color) -> None`

      Set the color of a single pixel at the specified coordinates to be an ``RGB``,
      ``RGBA``, string (for :doc:`color_list`), or mapped integer color value. If the Surface
      does not have per pixel alphas, the alpha value is ignored. Setting pixels outside the
      Surface area or outside the Surface clipping will have no effect.

      Getting and setting pixels one at a time is generally too slow to be used
      in a game or realtime situation.

      This function will temporarily lock and unlock the Surface as needed.

      .. note:: If the surface is palettized, the pixel color will be set to the
                most similar color in the palette.

      .. versionchanged:: 2.3.1 can now also accept both float coordinates and Vector2s for pixels.

      .. ## Surface.set_at ##

   .. method:: get_at_mapped

      | :sl:`get the mapped color value at a single pixel`
      | :sg:`get_at_mapped((x, y)) -> Color`

      Return the integer value of the given pixel. If the pixel position is
      outside the area of the Surface an ``IndexError`` exception will be
      raised.

      This method is intended for pygame unit testing. It unlikely has any use
      in an application.

      This function will temporarily lock and unlock the Surface as needed.

      .. versionaddedold:: 1.9.2

      .. versionchanged:: 2.3.1 can now also accept both float coordinates and Vector2s for pixels.

      .. ## Surface.get_at_mapped ##

   .. method:: get_palette

      | :sl:`get the color index palette for an 8-bit Surface`
      | :sg:`get_palette() -> [RGB, RGB, RGB, ...]`

      Return a list of up to 256 color elements that represent the indexed
      colors used in an 8-bit Surface. The returned list is a copy of the
      palette, and changes will have no effect on the Surface.

      Returning a list of ``Color(with length 3)`` instances instead of tuples.

      .. versionaddedold:: 1.9

      .. ## Surface.get_palette ##

   .. method:: get_palette_at

      | :sl:`get the color for a single entry in a palette`
      | :sg:`get_palette_at(index) -> RGB`

      Returns the red, green, and blue color values for a single index in a
      Surface palette. The index should be a value from 0 to 255.

      .. versionaddedold:: 1.9
         Returning ``Color(with length 3)`` instance instead of a tuple.

      .. ## Surface.get_palette_at ##

   .. method:: set_palette

      | :sl:`set the color palette for an 8-bit Surface`
      | :sg:`set_palette([RGB, RGB, RGB, ...]) -> None`

      Set the full palette for an 8-bit Surface. This will replace the colors in
      the existing palette. A partial palette can be passed and only the first
      colors in the original palette will be changed.
      
      This function has no effect on a Surface with more than 8-bits per pixel.

      .. ## Surface.set_palette ##

   .. method:: set_palette_at

      | :sl:`set the color for a single index in an 8-bit Surface palette`
      | :sg:`set_palette_at(index, RGB) -> None`

      Set the palette value for a single entry in a Surface palette. The index
      should be a value from 0 to 255.
      
      This function has no effect on a Surface with more than 8-bits per pixel.

      .. ## Surface.set_palette_at ##

   .. method:: map_rgb

      | :sl:`convert a color into a mapped color value`
      | :sg:`map_rgb(Color) -> mapped_int`

      Convert an ``RGBA`` color into the mapped integer value for this Surface.
      The returned integer will contain no more bits than the bit depth of the
      Surface. Mapped color values are not often used inside pygame, but can be
      passed to most functions that require a Surface and a color.

      See the Surface object documentation for more information about colors
      and pixel formats.

      .. ## Surface.map_rgb ##

   .. method:: unmap_rgb

      | :sl:`convert a mapped integer color value into a Color`
      | :sg:`unmap_rgb(mapped_int) -> Color`

      Convert an mapped integer color into the ``RGB`` color components for
      this Surface. Mapped color values are not often used inside pygame, but
      can be passed to most functions that require a Surface and a color.

      See the Surface object documentation for more information about colors
      and pixel formats.

      .. ## Surface.unmap_rgb ##

   .. method:: set_clip

      | :sl:`set the current clipping area of the Surface`
      | :sg:`set_clip(rect) -> None`
      | :sg:`set_clip(None) -> None`

      Each Surface has an active clipping area. This is a rectangle that
      represents the only pixels on the Surface that can be modified. If
      ``None`` is passed for the rectangle the full Surface will be available
      for changes.

      The clipping area is always restricted to the area of the Surface itself.
      If the clip rectangle is too large it will be shrunk to fit inside the
      Surface.

      .. ## Surface.set_clip ##

   .. method:: get_clip

      | :sl:`get the current clipping area of the Surface`
      | :sg:`get_clip() -> Rect`

      Return a rectangle of the current clipping area. The Surface will always
      return a valid rectangle that will never be outside the bounds of the
      image. If the Surface has had ``None`` set for the clipping area, the
      Surface will return a rectangle with the full area of the Surface.

      .. ## Surface.get_clip ##

   .. method:: subsurface

      | :sl:`create a new surface that references its parent`
      | :sg:`subsurface(Rect) -> Surface`

      Returns a new Surface that shares its pixels with its new parent. The new
      Surface is considered a child of the original. Modifications to either
      Surface pixels will effect each other. Surface information like clipping
      area and color keys are unique to each Surface.

      The new Surface will inherit the palette, color key, and alpha settings
      from its parent.

      It is possible to have any number of subsurfaces and subsubsurfaces on
      the parent. It is also possible to subsurface the display Surface if the
      display mode is not hardware accelerated.

      See :meth:`get_offset()` and :meth:`get_parent()` to learn more
      about the state of a subsurface.

      A subsurface will have the same class as the parent surface.

      .. ## Surface.subsurface ##

   .. method:: get_parent

      | :sl:`find the parent of a subsurface`
      | :sg:`get_parent() -> Surface`

      Returns the parent Surface of a subsurface. If this is not a subsurface
      then ``None`` will be returned.

      .. ## Surface.get_parent ##

   .. method:: get_abs_parent

      | :sl:`find the top level parent of a subsurface`
      | :sg:`get_abs_parent() -> Surface`

      Returns the parent Surface of a subsurface. If this is not a subsurface
      then this surface will be returned.

      .. ## Surface.get_abs_parent ##

   .. method:: get_offset

      | :sl:`find the position of a child subsurface inside a parent`
      | :sg:`get_offset() -> (x, y)`

      Get the offset position of a child subsurface inside of a parent. If the
      Surface is not a subsurface this will return (0, 0).

      .. ## Surface.get_offset ##

   .. method:: get_abs_offset

      | :sl:`find the absolute position of a child subsurface inside its top level parent`
      | :sg:`get_abs_offset() -> (x, y)`

      Get the offset position of a child subsurface inside of its top level
      parent Surface. If the Surface is not a subsurface this will return (0,
      0).

      .. ## Surface.get_abs_offset ##

   .. method:: get_size

      | :sl:`get the dimensions of the Surface`
      | :sg:`get_size() -> (width, height)`

      Return the width and height of the Surface in pixels.

      .. ## Surface.get_size ##

   .. method:: get_width

      | :sl:`get the width of the Surface`
      | :sg:`get_width() -> width`

      Return the width of the Surface in pixels.

      .. ## Surface.get_width ##

   .. method:: get_height

      | :sl:`get the height of the Surface`
      | :sg:`get_height() -> height`

      Return the height of the Surface in pixels.

      .. ## Surface.get_height ##

   .. method:: get_rect

      | :sl:`get the rectangular area of the Surface`
      | :sg:`get_rect(\**kwargs) -> Rect`

      Returns a new rectangle covering the entire surface. This rectangle will
      always start at (0, 0) with a width and height the same size as the image.

      You can pass keyword argument values to this function. These named values
      will be applied to the attributes of the Rect before it is returned. An
      example would be ``mysurf.get_rect(center=(100, 100))`` to create a
      rectangle for the Surface centered at a given position.

      .. ## Surface.get_rect ##

   .. method:: get_frect

      | :sl:`get the rectangular area of the Surface`
      | :sg:`get_frect(\**kwargs) -> FRect`
      
      This is the same as :meth:`Surface.get_rect` but returns an FRect. FRect is similar
      to Rect, except it stores float values instead.

      You can pass keyword argument values to this function. These named values
      will be applied to the attributes of the FRect before it is returned. An
      example would be ``mysurf.get_frect(center=(100.5, 100.5))`` to create a
      rectangle for the Surface centered at a given position.

      .. ## Surface.get_frect ##

   .. method:: get_bitsize

      | :sl:`get the bit depth of the Surface pixel format`
      | :sg:`get_bitsize() -> int`

      Returns the number of bits used to represent each pixel. This value may
      not exactly fill the number of bytes used per pixel. For example a 15 bit
      Surface still requires a full 2 bytes.

      .. ## Surface.get_bitsize ##

   .. method:: get_bytesize

      | :sl:`get the bytes used per Surface pixel`
      | :sg:`get_bytesize() -> int`

      Return the number of bytes used per pixel.

      .. ## Surface.get_bytesize ##

   .. method:: get_flags

      | :sl:`get the additional flags used for the Surface`
      | :sg:`get_flags() -> int`

      Returns a set of current Surface features. Each feature is a bit in the
      flags bitmask. Typical flags are ``RLEACCEL``, ``SRCALPHA``, and
      ``SRCCOLORKEY``.

      Here is a more complete list of flags. A full list can be found in
      ``SDL_video.h``

      ::

        SWSURFACE      0x00000000    # Surface is in system memory
        HWSURFACE      0x00000001    # (obsolete in pygame 2) Surface is in video memory
        ASYNCBLIT      0x00000004    # (obsolete in pygame 2) Use asynchronous blits if possible

      See :func:`pygame.display.set_mode()` for flags exclusive to the
      display surface.

      Used internally (read-only)

      ::

        HWACCEL        0x00000100    # Blit uses hardware acceleration
        SRCCOLORKEY    0x00001000    # Blit uses a source color key
        RLEACCELOK     0x00002000    # Private flag
        RLEACCEL       0x00004000    # Surface is RLE encoded
        SRCALPHA       0x00010000    # Blit uses source alpha blending
        PREALLOC       0x01000000    # Surface uses preallocated memory

      .. ## Surface.get_flags ##

   .. method:: get_pitch

      | :sl:`get the number of bytes used per Surface row`
      | :sg:`get_pitch() -> int`

      Return the number of bytes separating each row in the Surface. Surfaces
      in video memory are not always linearly packed. Subsurfaces will also
      have a larger pitch than their real width.

      This value is not needed for normal pygame usage.

      .. ## Surface.get_pitch ##

   .. method:: get_masks

      | :sl:`the bitmasks needed to convert between a color and a mapped integer`
      | :sg:`get_masks() -> (R, G, B, A)`

      Returns the bitmasks used to isolate each color in a mapped integer.

      This value is not needed for normal pygame usage.

      .. ## Surface.get_masks ##

   .. method:: set_masks

      | :sl:`set the bitmasks needed to convert between a color and a mapped integer`
      | :sg:`set_masks((r,g,b,a)) -> None`

      This is not needed for normal pygame usage.

      .. note:: Starting in pygame 2.0, the masks are read-only and
         accordingly this method will raise a TypeError if called.

      .. deprecatedold:: 2.0.0

      .. versionaddedold:: 1.8.1

      .. ## Surface.set_masks ##

   .. method:: get_shifts

      | :sl:`the bit shifts needed to convert between a color and a mapped integer`
      | :sg:`get_shifts() -> (R, G, B, A)`

      Returns the pixel shifts need to convert between each color and a mapped
      integer.

      This value is not needed for normal pygame usage.

      .. ## Surface.get_shifts ##

   .. method:: set_shifts

      | :sl:`sets the bit shifts needed to convert between a color and a mapped integer`
      | :sg:`set_shifts((r,g,b,a)) -> None`

      This is not needed for normal pygame usage.

      .. note:: Starting in pygame 2.0, the shifts are read-only and
         accordingly this method will raise a TypeError if called.

      .. deprecatedold:: 2.0.0

      .. versionaddedold:: 1.8.1

      .. ## Surface.set_shifts ##

   .. method:: get_losses

      | :sl:`the significant bits used to convert between a color and a mapped integer`
      | :sg:`get_losses() -> (R, G, B, A)`

      Return the least significant number of bits stripped from each color in a
      mapped integer.

      This value is not needed for normal pygame usage.

      .. ## Surface.get_losses ##

   .. method:: get_bounding_rect

      | :sl:`find the smallest rect containing data`
      | :sg:`get_bounding_rect(min_alpha = 1) -> Rect`

      Returns the smallest rectangular region that contains all the pixels in
      the surface that have an alpha value greater than or equal to the minimum
      alpha value.

      This function will temporarily lock and unlock the Surface as needed.

      .. versionaddedold:: 1.8

      .. ## Surface.get_bounding_rect ##

   .. method:: get_view

      | :sl:`return a buffer view of the Surface's pixels.`
      | :sg:`get_view(<kind>='2') -> BufferProxy`

      Return an object which exports a surface's internal pixel buffer as
      a C level array struct, Python level array interface or a C level
      buffer interface. The new buffer protocol is supported.

      The kind argument is the length 1 string '0', '1', '2', '3',
      'r', 'g', 'b', or 'a'. The letters are case insensitive;
      'A' will work as well. The argument can be either a Unicode or byte (char)
      string. The default is '2'.

      '0' returns a contiguous unstructured bytes view. No surface shape
      information is given. A ``ValueError`` is raised if the surface's pixels
      are discontinuous.

      '1' returns a (surface-width * surface-height) array of continuous
      pixels. A ``ValueError`` is raised if the surface pixels are
      discontinuous.

      '2' returns a (surface-width, surface-height) array of raw pixels.
      The pixels are surface-bytesize-d unsigned integers. The pixel format is
      surface specific. The 3 byte unsigned integers of 24 bit surfaces are
      unlikely accepted by anything other than other pygame functions.

      '3' returns a (surface-width, surface-height, 3) array of ``RGB`` color
      components. Each of the red, green, and blue components are unsigned
      bytes. Only 24-bit and 32-bit surfaces are supported. The color
      components must be in either ``RGB`` or ``BGR`` order within the pixel.

      'r' for red, 'g' for green, 'b' for blue, and 'a' for alpha return a
      (surface-width, surface-height) view of a single color component within a
      surface: a color plane. Color components are unsigned bytes. Both 24-bit
      and 32-bit surfaces support 'r', 'g', and 'b'. Only 32-bit surfaces with
      ``SRCALPHA`` support 'a'.

      The surface is locked only when an exposed interface is accessed.
      For new buffer interface accesses, the surface is unlocked once the
      last buffer view is released. For array interface and old buffer
      interface accesses, the surface remains locked until the BufferProxy
      object is released.

      .. versionaddedold:: 1.9.2

   .. method:: get_buffer

      | :sl:`acquires a buffer object for the pixels of the Surface.`
      | :sg:`get_buffer() -> BufferProxy`

      Return a buffer object for the pixels of the Surface. The buffer can be
      used for direct pixel access and manipulation. Surface pixel data is
      represented as an unstructured block of memory, with a start address
      and length in bytes. The data need not be contiguous. Any gaps are
      included in the length, but otherwise ignored.

      This method implicitly locks the Surface. The lock will be released when
      the returned :mod:`pygame.BufferProxy` object is garbage collected.

      .. versionaddedold:: 1.8

      .. ## Surface.get_buffer ##

   .. attribute:: _pixels_address

      | :sl:`pixel buffer address`
      | :sg:`_pixels_address -> int`

      The starting address of the surface's raw pixel bytes.

      .. versionaddedold:: 1.9.2

   .. method:: premul_alpha

      | :sl:`returns a copy of the surface with the RGB channels pre-multiplied by the alpha channel.`
      | :sg:`premul_alpha() -> Surface`

      Returns a copy of the initial surface with the red, green and blue color channels multiplied
      by the alpha channel. This is intended to make it easier to work with the BLEND_PREMULTIPLED
      blend mode flag of the blit() method. Surfaces which have called this method will only look
      correct after blitting if the BLEND_PREMULTIPLED special flag is used.

      It is worth noting that after calling this method, methods that return the colour of a pixel
      such as get_at() will return the alpha multiplied colour values. It is not possible to fully
      reverse an alpha multiplication of the colours in a surface as integer colour channel data
      is generally reduced by the operation (e.g. 255 x 0 = 0, from there it is not possible to reconstruct
      the original 255 from just the two remaining zeros in the colour and alpha channels).

      If you call this method, and then call it again, it will multiply the colour channels by the alpha channel
      twice. There are many possible ways to obtain a surface with the colour channels pre-multiplied by the
      alpha channel in pygame, and it is not possible to tell the difference just from the information in the pixels.
      It is completely possible to have two identical surfaces - one intended for pre-multiplied alpha blending and
      one intended for normal blending. For this reason we do not store state on surfaces intended for pre-multiplied
      alpha blending.

      Surfaces without an alpha channel cannot use this method and will return an error if you use
      it on them. It is best used on 32 bit surfaces (the default on most platforms) as the blitting
      on these surfaces can be accelerated by SIMD versions of the pre-multiplied blitter.

      In general pre-multiplied alpha blitting is faster then 'straight alpha' blitting and produces
      superior results when blitting an alpha surface onto another surface with alpha - assuming both
      surfaces contain pre-multiplied alpha colours.

      There is a `tutorial on premultiplied alpha blending here. <tutorials/en/premultiplied-alpha>`

      .. versionadded:: 2.1.4

      .. ## Surface.premul_alpha ##

   .. ## pygame.Surface ##


