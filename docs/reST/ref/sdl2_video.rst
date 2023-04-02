.. include:: common.txt

:mod:`pygame.sdl2_video`
========================

.. module:: pygame._sdl2.video
   :synopsis: Experimental pygame module for porting new SDL video systems

.. warning::
	This module isn't ready for prime time yet, it's still in development.
        These docs are primarily meant to help the pygame developers and super-early adopters
        who are in communication with the developers. This API will change.

| :sl:`Experimental pygame module for porting new SDL video systems`

.. function:: messagebox

   | :sl:`create a native GUI message box`
   | :sg:`messagebox(title, message, window=None, info=False, warn=False, buttons=('OK',), return_button=0, escape_button=0)`

   :param str or None title: A title string or None.
   :param str message: A message string.
   :param bool info: If ``True``, display an info message.
   :param bool warn: If ``True``, display a warning message.
   :param bool error: If ``True``, display an error message.
   :param tuple buttons: An optional sequence of buttons to show to the user (strings).
   :param int return_button: Button index to use if the return key is hit (-1 for none).
   :param int escape_button: Button index to use if the escape key is hit (-1 for none).
   :return: The index of the button that was pushed.

.. function:: get_drivers

   | :sl:`Yield info about the rendering drivers available for Renderer objects`
   | :sg:`get_drivers() -> Generator[RendererDriverInfo, None, None]`

.. class:: RendererDriverInfo

   | :sl:`pygame object encapsulating Renderer driver information`

   Attributes:
   
   ::
      
      name
      flags
      num_texture_formats
      max_texture_width
      max_texture_height

.. class:: Window

   | :sl:`pygame object that represents a window`
   | :sg:`Window(title="pygame", size=(640, 480), position=None, fullscreen=False, fullscreen_desktop=False, **kwargs) -> Window`

   :param str title: The title of the window.
   :param (int, int) size: The size of the window, in screen coordinates.
   :param (int, int) or int position: A tuple specifying the window position, or ``WINDOWPOS_CENTERED``, or ``WINDOWPOS_UNDEFINED``.
   :param bool fullscreen: Create a fullscreen window using the window size as the resolution (videomode change).
   :param bool fullscreen_desktop: Create a fullscreen window using the current desktop resolution
   :param bool opengl: Create a window with support for an OpenGL context. You will still need to create an OpenGL context separately.
   :param bool vulkan: Create a window with support for a Vulkan instance.
   :param bool hidden: Create a hidden window.
   :param bool borderless: Create a window without borders.
   :param bool resizable: Create a resizable window.
   :param bool minimized: Create a mimized window.
   :param bool maximized: Create a maximized window.
   :param bool input_grabbed: Create a window with a grabbed input focus.
   :param bool input_focus: Create a window with input focus.
   :param bool mouse_focus: Create a window with mouse focus.
   :param bool foreign: Marks a window not created by SDL.
   :param bool allow_highdpi: Create a window in high-DPI mode if supported (>= SDL 2.0.1)
   :param bool mouse_capture: Create a window that has the mouse captured (unrelated to INPUT_GRABBED, >= SDL 2.0.4)
   :param bool always_on_top: Create a window that is always on top (X11 only, >= SDL 2.0.5)
   :param bool skip_taskbar: Create a window that should not be added to the taskbar (X11 only, >= SDL 2.0.5)
   :param bool utility: Create a window that should be treated as a utility window (X11 only, >= SDL 2.0.5)
   :param bool tooltip: Create a window that should be treated as a tooltip (X11 only, >= SDL 2.0.5)
   :param bool popup_menu: Create a window that should be treated as a popup menu (X11 only, >= SDL 2.0.5)

   .. classmethod:: from_display_module
   
      | :sl:`Create a Window object using window data from display module`
      | :sg:`from_display_module() -> Window`

      Create a Window object that uses the same window data from the :mod:`pygame.display` module, created upon calling
      :func:`pygame.display.set_mode`.

   .. method:: get_grab

      | :sl:`Get the window's input grab state`
      | :sg:`get_grab() -> bool`

      Get the window's input grab state (whether the mouse is confined to the
      window).

   .. method:: set_grab

      | :sl:`Set the window's input grab state`
      | :sg:`set_grab(grabbed) -> None`

      :param bool grabbed: The new input grab state.

      When input is grabbed, the mouse is confined to the window.
      If the caller enables a grab while another window is currently grabbed,
      the other window loses its grab in favor of the caller's window.
   
   .. method:: get_relative_mouse_mode

      | :sl:`Get the window's relative mouse mode state`
      | :sg:`get_relative_mouse_mode() -> bool`

   .. method:: set_relative_mouse_mode

      | :sl:`Set the window's relative mouse mode state`
      | :sg:`set_relative_mouse_mode(enabled) -> None`

      :param bool enabled: The new relative mouse mode state.

      SDL2 docs: *"While the mouse is in relative mode, the cursor is hidden, the mouse position
      is constrained to the window, and SDL will report continuous relative mouse
      motion even if the mouse is at the edge of the window.*
      
      *This function will flush any pending mouse motion."*

      If :func:`pygame.mouse.set_visible` was called with ``True`` the input will be grabbed,
      and the mouse will enter endless relative motion mode.

   .. method:: set_windowed

      | :sl:`Enable windowed mode (exit fullscreen)`
      | :sg:`set_windowed() -> None`

      .. seealso:: :func:`set_fullscreen`

   .. method:: set_fullscreen

      | :sl:`Enter fullscreen`
      | :sg:`set_fullscreen(desktop=False) -> None`

      :param bool desktop: If ``True``, use the current desktop resolution.
         If ``False``, change the fullscreen resolution to the window size.

      .. seealso:: :meth:`set_windowed`.

   .. method:: get_title

      | :sl:`Get the window title`
      | :sg:`get_title() -> str`

      Get the window title, or an empty string if there is none.
   
   .. method:: set_title

      | :sl:`Set the window title`
      | :sg:`set_title() -> None`

      :param str title: The new window title.

   .. method:: destroy

      | :sl:`Destroy the window`
      | :sg:`destroy() -> None`

      Destroy the internal window data of this Window object. This method is called
      automatically when this Window object is garbage collected, so there usually aren't
      any reasons to call it manually.
      
      Other methods that try to manipulate that window data will raise an error.

   .. method:: hide

      | :sl:`Hide the window`
      | :sg:`hide() -> None`

   .. method:: show

      | :sl:`Show the window`
      | :sg:`show() -> None`

   .. method:: focus

      | :sl:`Set the window to be focused`
      | :sg:`focus(input_only=False) -> None`

      Raise the window above other windows and set the input focus.

      :param bool input_only: if ``True``, the window will be given input focus
                              but may be completely obscured by other windows.
                              Only supported on X11.

   .. method:: restore

      | :sl:`Restore the size and position of a minimized or maximized window`
      | :sg:`restore() -> None`

   .. method:: maximize

      | :sl:`Maximize the window`
      | :sg:`maximize() -> None`

   .. method:: minimize

      | :sl:`Minimize the window`
      | :sg:`maximize() -> None`

   .. method:: get_resizable

      | :sl:`Get whether the window is resizable`
      | :sg:`get_resizable() -> bool`
   
   .. method:: set_resizable

      | :sl:`Set whether the window is resizable`
      | :sg:`set_resizable(enabled) -> bool`

   .. method:: get_borderless

      | :sl:`Get whether the window is borderless`
      | :sg:`get_borderless() -> bool`
   
   .. method:: set_borderless

      | :sl:`Set whether the window is borderless`
      | :sg:`set_borderless(enabled) -> bool`

      .. :note:: You can't change the border state of a fullscreen window.

   .. method:: set_icon

      | :sl:`Set the icon for the window`
      | :sg:`set_icon(surface) -> None`

      :param Surface surface: A Surface to use as the icon.

   .. method:: get_window_id

      | :sl:`Get the unique window ID`
      | :sg:`get_window_id() -> int`

   .. method:: get_size

      | :sl:`Get the window size`
      | :sg:`get_size() -> (int, int)`
   
   .. method:: set_size

      | :sl:`Set the window size`
      | :sg:`set_size(size) -> None`

      :param (int, int) size: The new window size.

   .. method:: get_position

      | :sl:`Get the window's screen position`
      | :sg:`get_position() -> (int, int)`	
   
   .. method:: set_position

      | :sl:`Set the window's screen position`
      | :sg:`set_position(position) -> None`

      :param (int, int) or int position: The coordinates as an x, y tuple, or
         as ``WINDOWPOS_CENTERED`` to center the window.

   .. method:: get_opacity

      | :sl:`Get the window opacity`
      | :sg:`get_opacity() -> float`

      Get the window opacity, a floating point value between 0.0 (fully transparent)
      and 1.0 (fully opaque).

   .. method:: set_opacity

      | :sl:`Set the window opacity`
      | :sg:`set_opacity(opacity) -> None`

      :param float opacity: The new opacity value between 0.0
         (fully transparent) and 1.0 (fully opaque).

   .. method:: get_display_index

      | :sl:`Get the index of the display that owns the window`
      | :sg:`get_display_index() -> int`

   .. method:: set_modal_for

      | :sl:`Set the window as a modal for a parent window`
      | :sg:`set_modal_for(parent) -> None`

      :param Window parent: The parent window.
      
      This function is only supported on X11.


.. class:: Texture	

   | :sl:`pygame object that represents a texture`
   | :sg:`Texture(renderer, size, depth=0, static=False, streaming=False, target=False, scale_quality=None) -> Texture`

   :param Renderer renderer: The rendering context for the texture.
   :param tuple size: The width and height for the texture.
   :param int depth: The pixel format (0 to use the default).
   :param bool static: Initialize the texture as static (changes rarely, not lockable).
   :param bool streaming: Initialize the texture as streaming (changes frequently, lockable).
   :param bool target: Initialize the texture as target (can be used as a rendering target).
   :param int scale_quality: Set the texture scale quality. Can be 0
       (nearest pixel sampling), 1 (linear filtering, supported by OpenGL and Direct3D)
       and 2 (anisotropic filtering, supported by Direct3D)

   One of ``static``, ``streaming``, or ``target`` can be set
   to ``True``. If all are ``False``, then ``static`` is used.


   Texture objects provide a platform-agnostic API for working with GPU textures.
   They are stored in GPU video memory (VRAM), and are therefore very fast to
   rotate and resize when drawn unto a :class:`Renderer`
   (an object that manages a rendering context inside a :class:`Window`) on most GPUs.

   Since textures are stored in GPU video memory, they aren't as easy to modify as the image data of
   :class:`pygame.Surface` objects, which reside in RAM.
   
   Textures can be modified in 2 ways:
   
      * By drawing other textures unto them, which is achieved by marking them as "target" textures, and temporarily setting them as the rendering target of their Renderer object.
      
      * By updating them with a Surface.
         **WARNING:** This is a slow operation, as it requires image data to be uploaded from RAM to VRAM, a generally slow process.
      
   .. staticmethod:: from_surface

      | :sl:`Create a texture from an existing surface`
      | :sg:`from_surface(renderer, surface) -> Texture`

      :param Renderer renderer: Rendering context for the texture.
      :param Surface surface: The surface to create a texture from.

   .. method:: get_width

      | :sl:`Get the width of the Texture`
      | :sg:`get_width() -> int`

   .. method:: get_height

      | :sl:`Get the height of the Texture`
      | :sg:`get_height() -> int`
   
   .. method:: get_rect

      | :sl:`Get the rectangular area of the texture`
      | :sg:`get_rect(**kwargs) -> Rect`

      Like :meth:`pygame.Surface.get_rect`, returns a **new** rectangle covering the entire texture.
      This rectangle will always start at 0, 0 with a ``width`` and ``height`` the same size as the texture.

   .. method:: get_alpha

      | :sl:`Get the additional alpha value multiplied into draw operations`
      | :sg:`get_alpha() -> int`
   
   .. method:: set_alpha

      | :sl:`Set a additional alpha value multiplied into draw operations.`
      | :sg:`set_alpha(alpha) -> None`

      :param int alpha: The new alpha value. Must be between 0-255.

   .. method:: get_blend_mode

      | :sl:`Get the blend mode used for texture drawing operations`
      | :sg:`get_blend_mode() -> int`
   
   .. method:: set_blend_mode

      | :sl:`Set the blend mode used for texture drawing operations`
      | :sg:`set_blend_mode(blend_mode) -> None`

      :param int blend_mode: The blend mode. Can be set using one
                             of the ``BLENDMODE_*`` constants or a custom one. 

   .. method:: get_color

      | :sl:`Get the additional color value multiplied into texture drawing operations`
      | :sg:`get_color() -> Color`
   
   .. method:: set_color

      | :sl:`Set an additional color value multiplied into texture drawing operations`
      | :sg:`set_color(color) -> None`

   .. method:: draw

      | :sl:`Copy a portion of the texture to the rendering target`
      | :sg:`draw(srcrect=None, dstrect=None, angle=0, origin=None, flip_x=False, flip_y=False) -> None`

      :param srcrect: The source rectangle on the texture, or ``None`` for the entire
                      texture.
      :param dstrect: The destination rectangle on the rendering target, or ``None`` for
                      the entire rendering target. The texture will be stretched to fill
                      ``dstrect``.
      :param float angle: The angle (in degrees) to rotate dstrect around (clockwise).
      :param origin: The point around which dstrect will be rotated.
                     If ``None``, it will equal the center: (dstrect.w/2, dstrect.h/2).
      :param bool flip_x: Flip the drawn texture portion horizontally (x - axis).
      :param bool flip_y: Flip the drawn texture portion vertically (y - axis).

   .. method:: get_renderer

      | :sl:`Get the renderer associated with the Texture`
      | :sg:`renderer -> Renderer`

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

      | :sl:`Update the texture with Surface (WARNING: Slow operation, use sparingly)`
      | :sg:`update(surface, area=None) -> None`

      :param Surface surface: The source surface.
      :param area: The rectangular area of the texture to update.

      This is a fairly slow function, intended for use with static textures that do not change often.

      If the texture is intended to be updated often,
      it is preferred to create the texture as streaming and use the locking functions.

      While this function will work with streaming textures,for optimization reasons you may not
      get the pixels back if you lock the texture afterward.
 
.. class:: Image

   | :sl:`pygame object that represents a portion of a texture`
   | :sg:`Image(texture_or_image, srcrect=None) -> Image`

   An Image object represents a portion of a :class:`Texture`. Specifically, they can be used
   to store and manipulate arguments for :meth:`Texture.draw` in a more user friendly way.

   :param Texture | Image texture_or_image: The Texture or an existing Image object to create the Image from.
   :param srcrect: The rectangular portion of the Texture or Image object passed to ``texture_or_image``.

   .. method:: get_origin

      | :sl:`Get the Image's origin of rotation`
      | :sg:`get_origin() -> (float, float) or None`

      Get the Image's origin of rotation, a 2D coordinate relative to the topleft coordinate of the Image's rectangular area.
      
      An origin of ``None`` means no origin was set and the Image will be rotated around
      its center.
   
   .. method:: set_origin

      | :sl:`Set the Image's origin of rotation`
      | :sg:`set_origin(origin) -> None`

      :param origin: The new origin, a 2D coordinate relative to the topleft coordinate of the Image's rectangular area.

      An origin of ``None`` means the Image will be rotated around its center.

   .. method:: get_rect

      | :sl:`Get the rectangular area of the Image`
      | :sg:`get_rect() -> Rect`

      The returned :class:`Rect` object
      might contain position information relative to the bounds of the :class:`Texture` or
      Image object the Image was created from.

   .. method:: draw

      | :sl:`Copy a portion of the Image to the rendering target.`
      | :sg:`draw(srcrect=None, dstrect=None) -> None`

   .. attribute:: angle

      | :sl:`Gets and sets the angle the Image draws itself with.`
      | :sg:`angle -> float`

   .. attribute:: flip_x

      | :sl:`Gets and sets whether the Image is flipped on the x axis.`
      | :sg:`flip_x -> bool`

   .. attribute:: flip_y

      | :sl:`Gets and sets whether the Image is flipped on the y axis.`
      | :sg:`flip_y -> bool`

   .. method:: get_color

      | :sl:`Get the Image color modifier`
      | :sg:`get_color() -> Color`
   
   .. method:: set_color

      | :sl:`Set the Image color modifier`
      | :sg:`set_color(color) -> None`

   .. method:: get_alpha

      | :sl:`Get the Image alpha modifier`
      | :sg:`get_alpha() -> int`
   
   .. method:: set_alpha

      | :sl:`Set the Image alpha modifier`
      | :sg:`set_alpha(alpha) -> None`

      :param int alpha: The new alpha value. Must be between 0-255.

   .. method:: get_blend_mode

      | :sl:`Get the Image blend mode modifier`
      | :sg:`get_blend_mode() -> int`
   
   .. method:: set_blend_mode

      | :sl:`Set the Image blend mode modifier`
      | :sg:`set_blend_mode(blend_mode) -> None`

      :param int blend_mode: The blend mode. Can be set using one
                             of the ``BLENDMODE_*`` constants or a custom one. 

   .. attribute:: texture

      | :sl:`Gets and sets the Texture the Image is based on.`
      | :sg:`texture -> Texture`

   .. attribute:: srcrect

      | :sl:`Gets and sets the Rect the Image is based on.`
      | :sg:`srcrect -> Rect`

.. class:: Renderer

   | :sl:`pygame object wrapping a 2D rendering context for a window`
   | :sg:`Renderer(window, index=-1, accelerated=-1, vsync=False, target_texture=False) -> Renderer`

   Create a 2D rendering context for a window.

   :param Window window: The window unto which the rendering context should be placed.
   :param int index: The index of rendering driver to initialize, or -1 to init the first
                     supporting the requested options.
   :param int accelerated: If 1, the renderer uses hardware acceleration.
                           if 0, the renderer is a software fallback.
                           -1 gives precedence to renderers using hardware acceleration.
   :param bool vsync: If ``True`` :meth:`Renderer.present` is synchronized with the refresh rate.
   :param bool target_texture: Whether the renderer should support setting :class:`Texture` objects
                               as target textures, to enable drawing unto them. 


   :class:`Renderer` objects provide a cross-platform API for rendering 2D graphics unto a :class:`Window`,
   by using either Metal (MacOS), OpenGL (MacOS, Windows, Linux) or Direct3D (Windows) rendering drivers,
   depending on what is set or is available on a system during their creation.

   They can be used to draw both :class:`Texture` objects and simple points, lines and rectangles
   (which are colored based on :attr:`Renderer.draw_color`).

   If configured correctly, Renderer objects can have a :class:`Texture` object temporarily set as a target
   texture (the Texture object must have been created with target texture usage support), which allows those
   textures to be drawn unto. 

   To present drawn content unto the window, :meth:`Renderer.present` should be called. :meth:`Renderer.clear`
   should be called to clear any drawn content with the set Renderer draw color.

   When things are drawn unto Renderer objects, an internal batching system is used to batch those "draw
   calls" together, to have all of them be processed in one go when :meth:`Renderer.present` is called. This
   is unlike :class:`pygame.Surface` objects, on which modifications via blitting occur immediately, but lends
   well to the behavior of GPUs, as draw calls can be expensive on low-end models. Therefore, batching drawing
   operations is preferred where possible.

   .. classmethod:: from_window

      | :sl:`Create a Renderer from an existing window`
      | :sg:`from_window(window) -> Renderer`

   .. method:: get_draw_blend_mode

      | :sl:`Get the blend mode used for primitive drawing operations`
      | :sg:`get_draw_blend_mode() -> int`
   
   .. method:: set_draw_blend_mode

      | :sl:`Set the blend mode used for primitive drawing operations`
      | :sg:`set_draw_blend_mode(blend_mode) -> None`

      :param int blend_mode: The blend mode. Can be set using one
                             of the ``BLENDMODE_*`` constants or a custom one. 

   .. method:: get_draw_color

      | :sl:`Get the draw color used for primitive drawing operations`
      | :sg:`get_draw_color() -> Color`
   
   .. method:: set_draw_color

      | :sl:`Set the draw color used for primitive drawing operations`
      | :sg:`set_draw_color(color) -> None`

   .. method:: clear

      | :sl:`Clear the current rendering target with the draw color`
      | :sg:`clear() -> None`

   .. method:: present

      | :sl:`Update the screen with any rendering performed since the previous call`
      | :sg:`present() -> None`

   .. method:: get_viewport

      | :sl:`Get the drawing area on the rendering target`
      | :sg:`get_viewport() -> Rect`

   .. method:: set_viewport

      | :sl:`Set the drawing area on the rendering target`
      | :sg:`set_viewport(area) -> None`

      :param area: A :class:`pygame.Rect` or tuple representing the
                  drawing area on the target, or ``None`` to use the
                  entire area of the current rendering target.     

   .. method:: get_logical_size

      | :sl:`Get the logical Renderer size (a device independent resolution for rendering)`
      | :sg:`get_logical_size() -> (int, int)`
   
   .. method:: set_logical_size

      | :sl:`Set the logical Renderer size (a device independent resolution for rendering)`
      | :sg:`set_logical_size(size) -> None`
      
      :param size: The new logical size.

   .. method:: get_scale

      | :sl:`Get the drawing scale for the current rendering target`
      | :sg:`get_scale() -> (float, float)`
   
   .. method:: set_scale

      | :sl:`Set the drawing scale for the current rendering target`
      | :sg:`set_scale(scale) -> None`

   .. method:: get_target

      | :sl:`Get the current rendering target`
      | :sg:`get_target() -> Texture or None`

      A value of ``None`` means that no custom rendering target was set and the Renderer's window
      will be drawn unto.
   
   .. method:: set_target

      | :sl:`Set the current rendering target`
      | :sg:`set_target(target) -> None`

      :param Texture | None target: The :class:`Texture` object to use as a rendering target, or ``None``
                                    to revert back to the default target (the window). 

   .. method:: blit

      | :sl:`Draw textures using a Surface-like method`
      | :sg:`blit(source, dest, area=None, special_flags=0)-> Rect`

      For compatibility purposes. Draw :class:`Texture` objects unto the Renderer using a method signature
      similar to :meth:`pygame.Surface.blit`.

      :param source: A :class:`Texture` or :class:`Image` to draw.
      :param dest: The drawing destination on the rendering target.
      :param area: The portion of the source texture or image to draw from.
      :param special_flags: have no effect at this moment.

      Textures created by different Renderers cannot shared with each other!

   .. method:: draw_line

      | :sl:`Draws a line.`
      | :sg:`draw_line(p1, p2) -> None`

   .. method:: draw_point

      | :sl:`Draws a point.`
      | :sg:`draw_point(point) -> None`

   .. method:: draw_rect

      | :sl:`Draws a rectangle.`
      | :sg:`draw_rect(rect)-> None`

   .. method:: fill_rect

      | :sl:`Fills a rectangle.`
      | :sg:`fill_rect(rect)-> None`

   .. method:: to_surface

      | :sl:`Read pixels from current rendering target and create a Surface (WARNING: Slow operation, use sparingly)`
      | :sg:`to_surface(surface=None, area=None)-> Surface`

      Read pixel data from the current rendering target and return a :class:`pygame.Surface` containing it.

      :param Surface surface: A :class:`pygame.Surface` object to read the pixel data into.
                     It must be large enough to fit the area, otherwise ``ValueError`` is
                     raised.
                     If set to ``None``, a new surface will be created.
      :param area: The area of the screen to read pixels from. The area is
                  clipped to fit inside the viewport.
                  If ``None``, the entire viewport is used.
      
      **WARNING**: This is a very slow operation, and should not be used frequently.

   .. method:: draw_triangle

      | :sl:`Draw a triangle`
      | :sg:`draw_triangle(p1, p2, p3) -> None`

   .. method:: fill_triangle

      | :sl:`Fill a triangle`
      | :sg:`fill_triangle(p1, p2, p3) -> None`

   .. method:: draw_quad

      | :sl:`Draw a quad`
      | :sg:`draw_quad(p1, p2, p3, p4) -> None`

   .. method:: fill_quad

      | :sl:`Fill a quad`
      | :sg:`fill_quad(p1, p2, p3, p4) -> None`


   .. method:: compose_custom_blend_mode
   
      | :sl:`Compose a custom blend mode`
      | :sg:`compose_custom_blend_mode(color_mode, alpha_mode) -> int`

      Compose a custom blend mode.
      See https://wiki.libsdl.org/SDL2/SDL_ComposeCustomBlendMode for more information.

      :param color_mode: A tuple ``(srcColorFactor, dstColorFactor, colorOperation)``
      :param alpha_mode: A tuple ``(srcAlphaFactor, dstAlphaFactor, alphaOperation)``
      
      :return: A blend mode to be used with :meth:`Renderer.set_draw_blend_mode` and :meth:`Texture.set_blend_mode`.