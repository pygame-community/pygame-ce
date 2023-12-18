.. include:: common.txt

====================
:mod:`special flags`
====================

What Are Special Flags?
=======================

    **Special flags are a means of controlling how a** :class:`Surface` **is drawn onto another**.
    They can be used to create visual effects, such as glowing particles, or to perform surface
    masking or manipulation.
    They are used with the following methods:

        - :meth:`pygame.Surface.blit`
        - :meth:`pygame.Surface.blits`
        - :meth:`pygame.Surface.fblits`
        - :meth:`pygame.Surface.fill`

    Specifically they are passed as the ``special_flags`` argument of these methods by using
    ``pygame.BLEND_*`` constants and allow you to choose how the colors of the surfaces are
    combined or blended together. Different flags can produce widely different results, so
    it is important to experiment to understand how they work.

    By default, surfaces are drawn without any special flags, meaning they will be drawn based
    on their bit ``depth`` and ``colorkey``:

        - If the ``Surface`` has a ``colorkey``, the pixels matching the ``colorkey`` will be transparent.

        - If the ``Surface`` has a per-pixel or global alpha value, the alpha value will be used to blend the
          pixels with the ``Surface`` below.

        - If the ``Surface`` doesn't have a ``colorkey`` or alpha value, the pixels will be opaque, meaning
          that the ``Surface`` will effectively overwrite the pixels of the ``Surface`` below.

    The default drawing mode has its own flag: ``BLENDMODE_NONE`` (``0``).

Special Flags List
==================

**Blending without Alpha Channel (RGB)**

----

    .. versionaddedold:: 1.8 / 1.8.1

       - ``BLEND_ADD`` / ``BLEND_RGB_ADD``
           Adds the source color channels to the destination color channels, clamped to a maximum of 255.
           The result color is always a lighter color.

       - ``BLEND_SUB`` / ``BLEND_RGB_SUB``
           Subtracts the source color channels from the destination color channels, clamped to a minimum of 0.
           The result color is always a darker color.

       - ``BLEND_MULT`` / ``BLEND_RGB_MULT``
           Multiplies the destination color channels by the source color channels, divided by 256 (or >> 8).
           The result color is always a darker color.

       - ``BLEND_MIN`` / ``BLEND_RGB_MIN``
           Takes the minimum value between the source and destination color channels.

       - ``BLEND_MAX`` / ``BLEND_RGB_MAX``
           Takes the maximum value of each color channel

**Blending with Alpha Channel (RGBA)**

----

    .. versionaddedold:: 1.8.1

       - ``BLEND_RGBA_ADD``
           Works like ``BLEND_RGB_ADD``, but also adds the alpha channel.

       - ``BLEND_RGBA_SUB``
           Works like ``BLEND_RGB_SUB``, but also subtracts the alpha channel.

       - ``BLEND_RGBA_MULT``
           Works like ``BLEND_RGB_MULT``, but also multiplies the alpha channel.

       - ``BLEND_RGBA_MIN``
           Works like ``BLEND_RGB_MIN``, but also minimizes the alpha channel.

       - ``BLEND_RGBA_MAX``
           Works like ``BLEND_RGB_MAX``, but also maximizes the alpha channel.

**Special Alpha Blending (RGBA)**

----

    .. versionaddedold:: 1.9.2

       - ``BLEND_PREMULTIPLIED``
           Uses premultiplied alpha blending for slightly faster blits and more
           accurate blending results when the color channels are already multiplied
           by the surface alpha channel.
           You should only use this blend mode if you previously premultiplied the Surface with
           :meth:`pygame.Surface.premul_alpha()`, or if you know that the Surface was already 
           created or loaded in with premultiplied alpha colors. You can read more about the 
           advantages of `premultiplied alpha blending 
           here <https://en.wikipedia.org/wiki/Alpha_compositing>`_.

    .. versionaddedold:: 2.0.0

       - ``BLEND_ALPHA_SDL2``
           Uses the SDL2 blitter for alpha blending, which may give slightly different
           results compared to the default blitter used in Pygame 1. This algorithm uses
           different approximations for alpha blending and supports Run-Length Encoding
           (RLE) on alpha-blended surfaces.

**Other (RGB / RGBA)**

----

       - ``BLENDMODE_NONE``
           It's the default drawing mode. It's equivalent to not passing any special flags.
