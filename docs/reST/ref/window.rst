.. include:: common.txt

:mod:`pygame.Window`
=====================

.. currentmodule:: pygame

.. class:: Window

   | :sl:`pygame object that represents a window`
   | :sg:`Window(title='pygame window', size=(640, 480), position=None, fullscreen=False, fullscreen_desktop=False, **kwargs) -> Window`

   The Window class (formerly known as _sdl2.video.Window), is an experimental
   feature of pygame-ce. This class allows for programs to drive multiple
   Windows on-screen at once, something not possible with the 
   :func:`pygame.display.set_mode` API. Not everything possible with
   :mod:`pygame.display` is possible yet in the Window API, but the new
   window class will continue to be developed, and we're excited to share
   the new functionality this class offers.

   :param str title: The title of the window.
   :param (int, int) size: The size of the window, in screen coordinates.
   :param (int, int) or int position: A tuple specifying the window position, or
                                      ``WINDOWPOS_CENTERED``, or ``WINDOWPOS_UNDEFINED``.
   :param bool fullscreen: Create a fullscreen window using the window size as
                           the resolution (videomode change).
   :param bool fullscreen_desktop: Create a fullscreen window using the current
                                   desktop resolution.
   :param bool opengl: Create a window with support for an OpenGL context. You
                       will still need to create an OpenGL context separately.
   :param bool vulkan: Create a window with support for a Vulkan instance.
   :param bool hidden: Create a hidden window.
   :param bool borderless: Create a window without borders.
   :param bool resizable: Create a resizable window.
   :param bool minimized: Create a mimized window.
   :param bool maximized: Create a maximized window.
   :param bool mouse_grabbed: Create a window with grabbed mouse input.
   :param bool keyboard_grabbed: Create a window with grabbed keyboard input.
   :param bool input_focus: Create a window with input focus.
   :param bool mouse_focus: Create a window with mouse focus.
   :param bool foreign: Marks a window not created by SDL.
   :param bool allow_highdpi: Create a window in high-DPI mode if supported.
   :param bool mouse_capture: Create a window that has the mouse captured
                              (unrelated to INPUT_GRABBED).
   :param bool always_on_top: Create a window that is always presented above
                              others.

   .. versionadded:: 2.4.0


   .. attribute:: grab_mouse

      | :sl:`Get or set the window's mouse grab mode`
      | :sg:`grab_mouse -> bool`

      When this attribute is set to ``True``, the window will try to confine the mouse
      cursor to itself.

      Note this only set the "mode" of grab. The mouse may be confined to another window
      depending on the window focus. To get if the mouse is currently restricted to this
      window, please use :attr:`mouse_grabbed`.

      .. seealso:: :attr:`mouse_grabbed`

      .. versionadded:: 2.4.0
   
   .. attribute:: grab_keyboard

      | :sl:`Get or set the window's keyboard grab mode`
      | :sg:`grab_keyboard -> bool`
      
      When this attribute is set to ``True``, the window will try to capture system 
      keyboard shortcuts like ``Alt+Tab`` or the ``Meta/Super`` key. 

      This attribute only set the "mode" of grab. The keyboard may be captured by
      another window depending on the window focus. To get if keyboard is currently 
      captured by this window, please use :attr:`keyboard_grabbed`.
      
      Note that not all system keyboard shortcuts can be captured by applications
      (one example is ``Ctrl+Alt+Del`` on Windows).

      When keyboard grab is enabled, pygame will continue to handle ``Alt+Tab`` when
      the window is full-screen to ensure the user is not trapped in your application.
      If you have a custom keyboard shortcut to exit fullscreen mode, you may suppress
      this behavior with an environment variable, e.g.
      ``os.environ["SDL_ALLOW_ALT_TAB_WHILE_GRABBED"] = "0"``.

      This attribute requires SDL 2.0.16+.

      .. seealso:: :attr:`keyboard_grabbed`

      .. versionadded:: 2.4.0
      
   .. attribute:: mouse_grabbed

      | :sl:`Get if the mouse cursor is confined to the window (**read-only**)`
      | :sg:`mouse_grabbed -> bool`

      Get if the mouse cursor is currently grabbed and confined to the window.

      Roughly equivalent to this expression:
         
      ::

         win.grab_mouse and (win is get_grabbed_window())
      
      .. seealso:: :attr:`grab_mouse`
      
      .. versionadded:: 2.4.0
   
   .. attribute:: keyboard_grabbed

      | :sl:`Get if the keyboard shortcuts are captured by the window (**read-only**)`
      | :sg:`keyboard_grabbed -> bool`

      Get if the keyboard shortcuts are currently grabbed and captured by the window.

      Roughly equivalent to this expression:
         
      ::

         win.grab_keyboard and (win is get_grabbed_window())
      
      This attribute requires SDL 2.0.16+.
      
      .. seealso:: :attr:`grab_keyboard`
      
      .. versionadded:: 2.4.0

   .. attribute:: title

      | :sl:`Get or set the window title`
      | :sg:`title -> str`

      Gets or sets the window title. An empty string means that no title is set.

   .. attribute:: resizable

      | :sl:`Get or set whether the window is resizable`
      | :sg:`resizable -> bool`

   .. attribute:: borderless

      | :sl:`Get or set whether the window is borderless`
      | :sg:`borderless -> bool`

      Gets or sets whether the window is borderless.

      .. note:: You can't change the border state of a fullscreen window.
   
   .. attribute:: always_on_top

      | :sl:`Get or set whether the window is always on top`
      | :sg:`always_on_top -> bool`

      Get or set whether the window is always on top.

      Setting the always-on-top mode requires SDL 2.0.16+.

      .. versionadded:: 2.3.1

   .. attribute:: id

      | :sl:`Get the unique window ID (**read-only**)`
      | :sg:`id -> int`
   
   .. attribute:: mouse_rect

      | :sl:`Get or set the mouse confinement rectangle of the window`
      | :sg:`mouse_rect -> Rect|None`

      Setting this attribute to a rect-like object confines the
      cursor to the specified area of this window.

      This attribute can be None, meaning that there is no mouse rect.
      
      Note that this does NOT grab the cursor, it only defines the area a
      cursor is restricted to when the window has mouse focus.

      .. versionadded:: 2.4.0

   .. attribute:: size

      | :sl:`Get or set the window size in pixels`
      | :sg:`size -> (int, int)`
   
   .. attribute:: minimum_size

      | :sl:`Get or set the minimum size of the window's client area`
      | :sg:`minimum_size -> (int, int)`

      Initial value in most cases is ``(0, 0)``. If :func:`from_display_module`
      was used to create the window and :func:`pygame.display.set_mode` was
      called with the ``SCALED`` flag, the initial value is the size used in
      that call.
      
      Raises a ``ValueError`` if negative values are provided or 
      if the width or height provided are greater than set 
      maximum width or height respectively. Unless maximum size 
      is ``(0, 0)`` (initial value).

      .. seealso:: :attr:`maximum_size`.

      .. versionadded:: 2.4.0
   
   .. attribute:: maximum_size

      | :sl:`Get or set the maximum size of the window's client area`
      | :sg:`maximum_size -> (int, int)`

      Initial value is ``(0, 0)``.

      Raises a ``ValueError`` if negative values are provided or 
      if the width or height provided are less than set minimum 
      width or height respectively.

      .. seealso:: :attr:`minimum_size`.

      .. versionadded:: 2.4.0

   .. attribute:: position

      | :sl:`Get or set the window position in screen coordinates`
      | :sg:`position -> (int, int) or WINDOWPOS_CENTERED or WINDOWPOS_UNDEFINED`

   .. attribute:: opacity

      | :sl:`Get or set the window opacity, between 0.0 (fully transparent) and 1.0 (fully opaque)`
      | :sg:`opacity -> float`

   .. classmethod:: from_display_module

      | :sl:`Create a Window object using window data from display module`
      | :sg:`from_display_module() -> Window`

      **DON'T USE THIS!** If you want to draw to a surface and use the window
      API, use :func:`Window.get_surface` and :func:`Window.flip`.

      Create a Window object that uses the same window data from the :mod:`pygame.display` module, created upon calling
      :func:`pygame.display.set_mode`.

      .. deprecated:: 2.4.0

   .. method:: get_surface

      | :sl:`Get the window surface`
      | :sg:`get_surface() -> Surface`

      Returns a "display surface" for this Window. The surface returned is
      analogous to the surface returned by :func:`pygame.display.set_mode`.

      This method allows software rendering (classic pygame rendering) on top
      of the Window API. This method should not be called when using hardware
      rendering (coming soon).

      Similarly to the "display surface" returned by :mod:`pygame.display`,
      this surface will change size with the Window, and will become invalid
      after the Window's destruction.
      
      .. seealso:: :func:`flip`

      .. versionadded:: 2.4.0
   
   .. method:: flip

      | :sl:`Update the display surface to the window.`
      | :sg:`flip() -> None`

      Update content from the display surface to the window. This is the Window
      class equivalent of :func:`pygame.display.flip`.

      This method allows software rendering (classic pygame rendering) on top
      of the Window API. This method should not be called when using hardware
      rendering (coming soon).

      Here is a runnable example of using ``get_surface`` and ``flip``:

      .. code-block:: python

         import pygame

         win = pygame.Window()
         surf = win.get_surface()  # get the window surface

         while True:
            for event in pygame.event.get():
               if event.type == pygame.QUIT:
                     pygame.quit()
                     raise SystemExit

            # draw something on the surface
            surf.fill("red")

            win.flip()  # update the surface to the window


      .. versionadded:: 2.4.0

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

   .. method:: destroy

      | :sl:`Destroy the window`
      | :sg:`destroy() -> None`

      Destroys the internal window data of this Window object. This method is
      called automatically when this Window object is garbage collected, so
      there usually aren't any reasons to call it manually.

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

      Raises the window above other windows and sets the input focus.

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

   .. method:: set_icon

      | :sl:`Set the window icon`
      | :sg:`set_icon(surface, /) -> None`

      Sets the window icon.

      :param Surface surface: A Surface to use as the icon.

   .. method:: set_modal_for

      | :sl:`Set the window as a modal for a parent window`
      | :sg:`set_modal_for(parent, /) -> None`

      :param Window parent: The parent window.
      
      .. note:: This function is only supported on X11.

   .. ## pygame.Window ##
