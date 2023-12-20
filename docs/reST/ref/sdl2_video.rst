.. include:: common.txt

:mod:`pygame.sdl2_video`
========================

.. module:: pygame._sdl2.video
   :synopsis: Experimental pygame module for porting new SDL video systems

.. warning::
	This module isn't ready for prime time yet, it's still in development.
        These docs are primarily meant to help the pygame developers and
        super-early adopters who are in communication with the developers.
        This API will change.

| :sl:`Experimental pygame module for porting new SDL video systems`

.. function:: messagebox

   | :sl:`Create a native GUI message box`
   | :sg:`messagebox(title, message, window=None, info=False, warn=False, buttons=('OK',), return_button=0, escape_button=0)`

   :param str title: A title string, or ``None`` to omit a title.
   :param str message: A message string.
   :param bool info: If ``True``, display an info message.
   :param bool warn: If ``True``, display a warning message.
   :param bool error: If ``True``, display an error message.
   :param tuple buttons: An optional sequence of button name strings to show to the user.
   :param int return_button: Button index to use if the return key is hit (``-1`` for none).
   :param int escape_button: Button index to use if the escape key is hit (``-1`` for none).
   :return: The index of the button that was pushed.

.. class:: RendererDriverInfo

   | :sl:`pygame object encapsulating Renderer driver information`

   Attributes:
   
   ::
      
      name
      flags
      num_texture_formats
      max_texture_width
      max_texture_height

.. function:: get_drivers

   | :sl:`Yield info about the rendering drivers available for Renderer objects`
   | :sg:`get_drivers() -> Iterator[RendererDriverInfo]`

.. function:: get_grabbed_window

   | :sl:`Get the window with input grab enabled`
   | :sg:`get_grabbed_window() -> Window or None`

   Gets the :class:`Window` with input grab enabled, if input is grabbed,
   otherwise ``None`` is returned.


.. class:: Window

   | :sl:`pygame object that represents a window`

   See :class:`pygame.Window`

.. class:: Texture	

   | :sl:`pygame object that represents a texture`
   | :sg:`Texture(renderer, size, depth=0, static=False, streaming=False, target=False, scale_quality=None) -> Texture`

   Creates an empty texture.

   :param Renderer renderer: The rendering context for the texture.
   :param tuple size: The width and height for the texture.
   :param int depth: The pixel format (``0`` to use the default).
   :param bool static: Initialize the texture as static
                       (changes rarely, not lockable).
   :param bool streaming: Initialize the texture as streaming
                          (changes frequently, lockable).
   :param bool target: Initialize the texture as target
                       (can be used as a rendering target).
   :param int scale_quality: Set the texture scale quality. Can be ``0``
                             (nearest pixel sampling), ``1``
                             (linear filtering, supported by OpenGL and Direct3D)
                             and ``2`` (anisotropic filtering, supported by Direct3D).

   One of ``static``, ``streaming``, or ``target`` can be set
   to ``True``. If all are ``False``, then ``static`` is used.


   :class:`Texture` objects provide a platform-agnostic API for working with GPU textures.
   They are stored in GPU video memory (VRAM), and are therefore very fast to
   rotate and resize when drawn onto a :class:`Renderer`
   (an object that manages a rendering context inside a :class:`Window`) on most GPUs.

   Since textures are stored in GPU video memory, they aren't as easy to modify
   as the image data of :class:`pygame.Surface` objects, which reside in RAM.
   
   Textures can be modified in 2 ways:
        
      * By drawing other textures onto them, achieved by marking them as "target" textures and setting them as the rendering target of their Renderer object (if properly configured and supported).
         
      * By updating them with a Surface.

      .. note::
         A :class:`pygame.Surface`-to-:class:`Texture` update is generally
         considered a slow operation, as it requires image data to be uploaded from
         RAM to VRAM, which can have a notable overhead cost.
   
   .. attribute:: renderer

      | :sl:`Get the renderer associated with the texture (**read-only**)`
      | :sg:`renderer -> Renderer`

   .. attribute:: width

      | :sl:`Get the width of the texture (**read-only**)`
      | :sg:`width -> int`

   .. attribute:: height

      | :sl:`Get the height of the texture (**read-only**)`
      | :sg:`height -> int`

   .. attribute:: alpha

      | :sl:`Get or set the additional alpha value multiplied into draw operations`
      | :sg:`alpha -> int`

   .. attribute:: blend_mode

      | :sl:`Get or set the blend mode for texture drawing operations`
      | :sg:`blend_mode -> int`

      Gets or sets the blend mode for the texture's drawing operations.
      Valid blend modes are any of the ``BLENDMODE_*`` constants or a custom one. 

   .. attribute:: color

      | :sl:`Get or set the additional color value multiplied into texture drawing operations`
      | :sg:`color -> Color`

   .. staticmethod:: from_surface

      | :sl:`Create a texture from an existing surface`
      | :sg:`from_surface(renderer, surface) -> Texture`

      :param Renderer renderer: Rendering context for the texture.
      :param Surface surface: The surface to create a texture from.

   .. method:: get_rect

      | :sl:`Get the rectangular area of the texture`
      | :sg:`get_rect(**kwargs) -> Rect`

      Like :meth:`pygame.Surface.get_rect`, this method returns a **new**
      :class:`pygame.Rect` covering the entire texture. It will always
      have a ``topleft`` of ``(0, 0)`` with a ``width`` and ``height`` the same size as the
      texture.

   .. method:: draw

      | :sl:`Copy a portion of the texture to the rendering target`
      | :sg:`draw(srcrect=None, dstrect=None, angle=0, origin=None, flip_x=False, flip_y=False) -> None`

      :param srcrect: The source rectangle on the texture, or ``None`` for the
                      entire texture.
      :param dstrect: The destination rectangle on the rendering target, or
                      ``None`` for the entire rendering target. The texture
                      will be stretched to fill ``dstrect``.
      :param float angle: The angle (in degrees) to rotate dstrect around
                          (clockwise).
      :param origin: The point around which dstrect will be rotated.
                     If ``None``, it will equal the center:
                     ``(dstrect.w/2, dstrect.h/2)``.
      :param bool flip_x: Flip the drawn texture portion horizontally (x - axis).
      :param bool flip_y: Flip the drawn texture portion vertically (y - axis).

   .. method:: draw_triangle

      | :sl:`Copy a triangle portion of the texture to the rendering target using the given coordinates`
      | :sg:`draw_triangle(p1_xy, p2_xy, p3_xy, p1_uv=(0.0, 0.0), p2_uv=(1.0, 1.0), p3_uv=(0.0, 1.0), p1_mod=(255, 255, 255, 255), p2_mod=(255, 255, 255, 255), p3_mod=(255, 255, 255, 255)) -> None`

      :param p1_xy: The first vertex coordinate on the rendering target.
      :param p2_xy: The second vertex coordinate on the rendering target.
      :param p3_xy: The third vertex coordinate on the rendering target.
      :param p1_uv: The first UV coordinate of the triangle portion.
      :param p2_uv: The second UV coordinate of the triangle portion.
      :param p3_uv: The third UV coordinate of the triangle portion.
      :param p1_mod: The first vertex color modulation.
      :param p2_mod: The second vertex color modulation.
      :param p3_mod: The third vertex color modulation.

   .. method:: draw_quad

      | :sl:`Copy a quad portion of the texture to the rendering target using the given coordinates`
      | :sg:`draw_quad(p1_xy, p2_xy, p3_xy, p4_xy, p1_uv=(0.0, 0.0), p2_uv=(1.0, 0.0), p3_uv=(1.0, 1.0), p4_uv=(0.0, 1.0), p1_mod=(255, 255, 255, 255), p2_mod=(255, 255, 255, 255), p3_mod=(255, 255, 255, 255), p4_mod=(255, 255, 255, 255)) -> None`

      :param p1_xy: The first vertex coordinate on the rendering target.
      :param p2_xy: The second vertex coordinate on the rendering target.
      :param p3_xy: The third vertex coordinate on the rendering target.
      :param p4_xy: The fourth vertex coordinate on the rendering target.
      :param p1_uv: The first UV coordinate of the quad portion.
      :param p2_uv: The second UV coordinate of the quad portion.
      :param p3_uv: The third UV coordinate of the quad portion.
      :param p4_uv: The fourth UV coordinate of the quad portion.
      :param p1_mod: The first vertex color modulation.
      :param p2_mod: The second vertex color modulation.
      :param p3_mod: The third vertex color modulation.
      :param p4_mod: The fourth vertex color modulation.

   .. method:: update

      | :sl:`Update the texture with Surface (slow operation, use sparingly)`
      | :sg:`update(surface, area=None) -> None`

      :param Surface surface: The source surface.
      :param area: The rectangular area of the texture to update.

      .. note::
         This is a fairly slow function, intended for use with static textures
         that do not change often.

         If the texture is intended to be updated often, it is preferred to create
         the texture as streaming and use the locking functions.

         While this function will work with streaming textures, for optimization
         reasons you may not get the pixels back if you lock the texture afterward.


.. class:: Image

   | :sl:`pygame object that represents a portion of a texture`
   | :sg:`Image(texture_or_image, srcrect=None) -> Image`

   Creates an Image.

   :param Texture | Image texture_or_image: The Texture or an existing Image
                                            object to create the Image from.
   :param srcrect: The rectangular portion of the Texture or Image object
                   passed to ``texture_or_image``.

   An :class:`Image` object represents a portion of a :class:`Texture`. Specifically,
   they can be used to store and manipulate arguments for :meth:`Texture.draw`
   in a more user-friendly way.

   .. attribute:: angle

      | :sl:`Get and set the angle the Image draws itself with`
      | :sg:`angle -> float`

   .. attribute:: flip_x

      | :sl:`Get or set whether the Image is flipped on the x axis`
      | :sg:`flip_x -> bool`

   .. attribute:: flip_y

      | :sl:`Get or set whether the Image is flipped on the y axis`
      | :sg:`flip_y -> bool`

   .. attribute:: color

      | :sl:`Get or set the Image color modifier`
      | :sg:`color -> Color`

   .. attribute:: alpha

      | :sl:`Get or set the Image alpha modifier (0-255)`
      | :sg:`alpha -> float`

   .. attribute:: blend_mode

      | :sl:`Get or set the blend mode for the Image`
      | :sg:`blend_mode -> int`

   .. attribute:: texture

      | :sl:`Get or set the Texture the Image is based on`
      | :sg:`texture -> Texture`

   .. attribute:: srcrect

      | :sl:`Get or set the Rect the Image is based on`
      | :sg:`srcrect -> Rect`

   .. attribute:: origin

      | :sl:`Get or set the Image's origin of rotation`
      | :sg:`origin -> (float, float) or None`

      Gets or sets the Image's origin of rotation, a 2D coordinate relative to
      the topleft coordinate of the Image's rectangular area.

      An origin of ``None`` means no origin was set and the Image will be
      rotated around its center.
   
   .. method:: get_rect

      | :sl:`Get the rectangular area of the Image`
      | :sg:`get_rect() -> Rect`

      .. note::
         The returned :class:`Rect` object might contain position information
         relative to the bounds of the :class:`Texture` or Image object it was
         created from.

   .. method:: draw

      | :sl:`Copy a portion of the Image to the rendering target`
      | :sg:`draw(srcrect=None, dstrect=None) -> None`

      :param srcrect: Source rectangle specifying a sub-Image, or ``None`` for the
                      entire Image.
      :param dstrect: Destination rectangle or position on the render target,
                      or ``None`` for entire target. The Image is stretched to
                      fill dstrect.


.. class:: Renderer

   | :sl:`pygame object wrapping a 2D rendering context for a window`
   | :sg:`Renderer(window, index=-1, accelerated=-1, vsync=False, target_texture=False) -> Renderer`

   Creates a 2D rendering context for a window.

   :param Window window: The window onto which the rendering context should be
                         placed.
   :param int index: The index of rendering driver to initialize, or ``-1`` to init
                     the first supporting the requested options.
   :param int accelerated: If 1, the renderer uses hardware acceleration.
                           if 0, the renderer is a software fallback.
                           ``-1`` gives precedence to renderers using hardware
                           acceleration.
   :param bool vsync: If ``True`` :meth:`Renderer.present` is synchronized with
                      the refresh rate.
   :param bool target_texture: Whether the renderer should support setting
                              :class:`Texture` objects as target textures, to
                              enable drawing onto them. 


   :class:`Renderer` objects provide a cross-platform API for rendering 2D
   graphics onto a :class:`Window`, by using either Metal (macOS), OpenGL
   (macOS, Windows, Linux) or Direct3D (Windows) rendering drivers, depending
   on what is set or is available on a system during their creation.

   They can be used to draw both :class:`Texture` objects and simple points,
   lines and rectangles (which are colored based on :attr:`Renderer.draw_color`).

   If configured correctly and supported by an underlying rendering driver, Renderer
   objects can have a :class:`Texture` object temporarily set as a target texture
   (the Texture object must have been created with target texture usage support),
   which allows those textures to be drawn onto. 

   To present drawn content onto the window, :meth:`Renderer.present` should be
   called. :meth:`Renderer.clear` should be called to clear any drawn content
   with the set Renderer draw color.

   When things are drawn onto Renderer objects, an internal batching system is
   used by default to batch those "draw calls" together, to have all of them be
   processed in one go when :meth:`Renderer.present` is called. This is unlike
   :class:`pygame.Surface` objects, on which modifications via blitting occur
   immediately, but lends well to the behavior of GPUs, as draw calls can be
   expensive on lower-end models.

   .. attribute:: draw_blend_mode

      | :sl:`Get or set the blend mode used for primitive drawing operations`
      | :sg:`draw_blend_mode -> int`   

   .. attribute:: draw_color

      | :sl:`Get or set the color used for primitive drawing operations`
      | :sg:`draw_color -> Color`

   .. attribute:: logical_size

      | :sl:`Get or set the logical Renderer size (a device independent resolution for rendering)`
      | :sg:`logical_size -> (int width, int height)`

   .. attribute:: scale

      | :sl:`Get the drawing scale for the current rendering target`
      | :sg:`scale -> (float, float)`

   .. attribute:: target

      | :sl:`Get or set the current rendering target`
      | :sg:`target -> Texture or None`

      Gets or sets the current rendering target.
      A value of ``None`` means that no custom rendering target was set and the
      Renderer's window will be used as the target.

   .. classmethod:: from_window

      | :sl:`Create a Renderer from an existing window`
      | :sg:`from_window(window) -> Renderer`

   .. method:: clear

      | :sl:`Clear the current rendering target with the drawing color`
      | :sg:`clear() -> None`

   .. method:: present

      | :sl:`Update the screen with any rendering performed since the previous call`
      | :sg:`present() -> None`

      Presents the composed backbuffer to the screen.
      Updates the screen with any rendering performed since the previous call.

   .. method:: get_viewport

      | :sl:`Get the drawing area on the rendering target`
      | :sg:`get_viewport() -> Rect`

   .. method:: set_viewport

      | :sl:`Set the drawing area on the rendering target`
      | :sg:`set_viewport(area) -> None`

      :param area: A :class:`pygame.Rect` or tuple representing the
                   drawing area on the target, or ``None`` to use the
                   entire area of the current rendering target. 

   .. method:: blit

      | :sl:`Draw textures using a Surface-like API`
      | :sg:`blit(source, dest, area=None, special_flags=0)-> Rect`

      For compatibility purposes. Draws :class:`Texture` objects onto the
      Renderer using a method signature similar to :meth:`pygame.Surface.blit`.

      :param source: A :class:`Texture` or :class:`Image` to draw.
      :param dest: The drawing destination on the rendering target.
      :param area: The portion of the source texture or image to draw from.
      :param special_flags: have no effect at this moment.

      .. note:: Textures created by different Renderers cannot shared with each other!

   .. method:: draw_line

      | :sl:`Draw a line`
      | :sg:`draw_line(p1, p2) -> None`

      :param p1: The line start point.
      :param p2: The line end point.

   .. method:: draw_point

      | :sl:`Draw a point`
      | :sg:`draw_point(point) -> None`

      :param point: The point's coordinate.

   .. method:: draw_rect

      | :sl:`Draw a rectangle outline`
      | :sg:`draw_rect(rect)-> None`

      :param rect: The :class:`pygame.Rect`-like rectangle to draw.

   .. method:: fill_rect

      | :sl:`Draw a filled rectangle`
      | :sg:`fill_rect(rect)-> None`

      :param rect: The :class:`pygame.Rect`-like rectangle to draw.

   .. method:: draw_triangle

      | :sl:`Draw a triangle outline`
      | :sg:`draw_triangle(p1, p2, p3) -> None`
      
      :param p1: The first triangle point.
      :param p2: The second triangle point.
      :param p2: The third triangle point.

   .. method:: fill_triangle

      | :sl:`Draw a filled triangle`
      | :sg:`fill_triangle(p1, p2, p3) -> None`

      :param p1: The first triangle point.
      :param p2: The second triangle point.
      :param p2: The third triangle point.

   .. method:: draw_quad

      | :sl:`Draw a quad outline`
      | :sg:`draw_quad(p1, p2, p3, p4) -> None`

      :param p1: The first quad point.
      :param p2: The second quad point.
      :param p2: The third quad point.
      :param p2: The fourth quad point.

   .. method:: fill_quad

      | :sl:`Draw a filled quad`
      | :sg:`fill_quad(p1, p2, p3, p4) -> None`

      :param p1: The first quad point.
      :param p2: The second quad point.
      :param p2: The third quad point.
      :param p2: The fourth quad point.

   .. method:: to_surface

      | :sl:`Read pixels from current rendering target and create a Surface (slow operation, use sparingly)`
      | :sg:`to_surface(surface=None, area=None)-> Surface`

      Read pixel data from the current rendering target and return a
      :class:`pygame.Surface` containing it.

      :param Surface surface: A :class:`pygame.Surface` object to read the pixel
                              data into. It must be large enough to fit the area, otherwise
                              ``ValueError`` is raised.
                              If set to ``None``, a new surface will be created.
      :param area: The area of the screen to read pixels from. The area is
                   clipped to fit inside the viewport.
                   If ``None``, the entire viewport is used.

      .. note::
         This is a very slow operation, due to the overhead of the VRAM to RAM
         data transfer and the cost of creating a potentially large
         :class:`pygame.Surface`. It should not be used frequently.

   .. method:: compose_custom_blend_mode
   
      | :sl:`Compose a custom blend mode`
      | :sg:`compose_custom_blend_mode(color_mode, alpha_mode) -> int`

      Compose a custom blend mode.
      See https://wiki.libsdl.org/SDL2/SDL_ComposeCustomBlendMode for more information.

      :param color_mode: A tuple ``(srcColorFactor, dstColorFactor, colorOperation)``
      :param alpha_mode: A tuple ``(srcAlphaFactor, dstAlphaFactor, alphaOperation)``
      
      :return: A blend mode to be used with :meth:`Renderer.set_draw_blend_mode` and :meth:`Texture.set_blend_mode`.