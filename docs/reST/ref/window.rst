.. include:: common.txt

:mod:`pygame.Window`
=====================

.. currentmodule:: pygame

.. class:: Window

   | :sl:`pygame object that represents a window`
   | :sg:`Window(title='pygame window', size=(640, 480), position=None, fullscreen=False, fullscreen_desktop=False, **kwargs) -> Window`

   The Window class (formerly known as _sdl2.video.Window), is a newly
   published feature of pygame-ce 2.5.2. This class allows for programs
   to drive multiple windows on-screen at once, something not possible with
   the :func:`pygame.display.set_mode` API. Not everything possible with
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
   :param bool opengl: Create a window with support for an OpenGL context.
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
   :param bool allow_high_dpi: Create a window in high-DPI mode if supported.
   :param bool mouse_capture: Create a window that has the mouse captured
                              (unrelated to INPUT_GRABBED).
   :param bool always_on_top: Create a window that is always presented above
                              others.
   :param bool utility: Create a window that doesn't appear in the task bar.

   Event behavior if one Window is created: When the close button is pressed,
   the ``QUIT`` event will be sent to the event queue.

   .. code-block:: python

     import pygame

     window = pygame.Window()

     while True:
       for event in pygame.event.get():
          if event.type == pygame.QUIT:
             pygame.quit()
             raise SystemExit

   Event behavior if multiple ``Window``\ s are created: When the close button is
   pressed, a ``WINDOWCLOSE`` event is sent. You need to explicitly destroy
   the window. Note that the event ``QUIT`` will only be sent if all
   ``Window``\ s have been destroyed.

   .. code-block:: python

     import pygame

     window1 = pygame.Window(position=(0,100))
     window2 = pygame.Window(position=(700,100))

     while True:
       for event in pygame.event.get():
         if event.type == pygame.WINDOWCLOSE:
           id = event.window.id
           print(f"WINDOWCLOSE event sent to Window #{id}.")
           event.window.destroy()

         if event.type == pygame.QUIT:
           print(f"Last window is destroyed. QUIT event was sent.")
           pygame.quit()
           raise SystemExit

   .. versionadded:: 2.4.0
   .. versionchanged:: 2.5.0 when ``opengl`` is ``True``, the ``Window`` has an OpenGL context created by pygame
   .. versionchanged:: 2.5.1 Window is now a base class, allowing subclassing


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

   .. attribute:: focused

      | :sl:`Get if the window is focused (**read-only**)`
      | :sg:`focused -> bool`

      Get if the window is currently focused. The same result can be achieved using
      the ``WINDOWFOCUSGAINED`` and ``WINDOWFOCUSLOST`` events.

      Use :meth:`focus` to focus and raise the window.

      .. versionadded:: 2.5.2

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

   .. attribute:: opengl

      | :sl:`Get if the window supports OpenGL`
      | :sg:`opengl -> bool`

      ``True`` if the ``Window`` has an OpenGL context associated with it, ``False`` otherwise

      .. versionadded:: 2.5.0

   .. attribute:: utility

      | :sl:`Get if the window is an utility window (**read-only**)`
      | :sg:`utility -> bool`

      ``True`` if the window doesn't appear in the task bar, ``False`` otherwise.
      This only works for X11 and Windows, for other platforms, creating ``Window(utility=True)`` won't change anything.

      .. versionadded:: 2.5.3

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

      Update pixel data from memory to be displayed in the window. This is the Window
      class equivalent of :func:`pygame.display.flip`.

      With ``get_surface()`` this method allows software rendering (classic pygame rendering) flipping pixel data
      from an associated surface in memory to be displayed in the window. Alternatively, when this window has an
      associated OpenGL context, this method will instead perform a GL buffer swap to the window.

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
                              Only supported on X11. This has been deprecated and
                              may be removed in a future version.

      .. deprecated:: 2.5.3 ``input_only`` argument

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

   .. method:: flash

      | :sl:`Flash a window to demand attention from the user`
      | :sg:`flash(operation, /) -> None`

      :param int operation: The flash operation.

      Supported flash operations are:
         * ``pygame.FLASH_CANCEL``: Cancel the current flash state if present
         * ``pygame.FLASH_BRIEFLY``: Flash for a short amount of time to get attention
         * ``pygame.FLASH_UNTIL_FOCUSED``: Keep flashing until the window is focused

      Window flashing requires SDL 2.0.16+. A :mod:`pygame.error` exception will be raised
      otherwise.

      .. note:: This function is only supported on Windows, X11, Wayland and Cocoa (MacOS).
         A :mod:`pygame.error` exception will be raised if it's not supported therefore it's
         advised to wrap it in a try block.

         .. code-block:: python

            import pygame
            window = pygame.Window()

            try:
               window.flash(pygame.FLASH_BRIEFLY)
            except pygame.error:
               print("Window flashing not supported")

      .. versionadded:: 2.5.2

   .. ## pygame.Window ##
