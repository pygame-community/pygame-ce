.. include:: common.txt

:mod:`pygame.window`
=====================

.. module:: pygame.window
   :synopsis: pygame module to control windows

| :sl:`pygame module to control windows`

.. function:: get_grabbed_window

   | :sl:`Get the current grabbed window`
   | :sg:`get_grabbed_window() -> Optional[Window]`

   Returns ``None`` if there is no grabbed window.

   .. ## pygame.window.get_grabbed_window ##

.. class:: Window

   | :sl:`pygame object that represents a window`
   | :sg:`Window(title='pygame window', size=(640, 480), position=WINDOWPOS_UNDEFINED, **flags)`

   :param str title: The title of the window.
   :param (int, int) size: The size of the window, in screen coordinates.
   :param (int, int) or int position: A tuple specifying the window position, or ``pygame.WINDOWPOS_CENTERED``, or ``pygame.WINDOWPOS_UNDEFINED``.
   :param bool fullscreen: Create a fullscreen window using the window size as the resolution (videomode change).
   :param bool fullscreen_desktop: Create a fullscreen window using the current desktop resolution
   :param bool opengl: Create a window with support for an OpenGL context. You will still need to create an OpenGL context separately.
   :param bool vulkan: Create a window with support for a Vulkan instance.
   :param bool metal: Create a window with support for Metal.
   :param bool hidden: Create a hidden window.
   :param bool borderless: Create a window without borders.
   :param bool resizable: Create a resizable window.
   :param bool minimized: Create a mimized window.
   :param bool maximized: Create a maximized window.
   :param bool mouse_grabbed: Create a window with a grabbed mouse input focus.
   :param bool keyboard_grabbed: Create a window with a grabbed keyboard input focus.
   :param bool allow_highdpi: Create a window in high-DPI mode if supported
   :param bool mouse_capture: Create a window that has the mouse captured (unrelated to ``mouse_grabbed``)
   :param bool always_on_top: Create a window that is always on top
   :param bool skip_taskbar: Create a window that should not be added to the taskbar
   :param bool utility: Create a window that should be treated as a utility window (X11 only)
   :param bool tooltip: Create a window that should be treated as a tooltip (X11 only)
   :param bool popup_menu: Create a window that should be treated as a popup menu (X11 only)

   .. classmethod:: from_display_module
   
      | :sl:`Create a Window object using window data from display module`
      | :sg:`from_display_module() -> Window`

      Create a Window object that uses the same window data from the :mod:`pygame.display` module, created upon calling
      :func:`pygame.display.set_mode`.

      .. ## Window.from_display_module ##

   .. method:: destroy

      | :sl:`Destroy the window`
      | :sg:`destroy() -> None`

      Destroy the internal window data of this Window object.

      .. ## Window.destroy ##

   .. method:: set_windowed

      | :sl:`Enable windowed mode (exit fullscreen)`
      | :sg:`set_windowed() -> None`

      .. seealso:: :func:`set_fullscreen`

      .. ## Window.set_windowed ##

   .. method:: set_fullscreen

      | :sl:`Enter fullscreen`
      | :sg:`set_fullscreen(desktop=False) -> None`

      :param bool desktop: If ``True``, use the current desktop resolution.
         If ``False``, change the fullscreen resolution to the window size.

      .. seealso:: :meth:`set_windowed`.

      .. ## Window.set_fullscreen ##
   
   .. method:: focus

      | :sl:`Set the window to be focused`
      | :sg:`focus(input_only=False) -> None`

      Raise the window above other windows and set the input focus.

      :param bool input_only: if ``True``, the window will be given input focus
                              but may be completely obscured by other windows.
                              Only supported on X11.

      .. ## Window.focus ##
   
   .. method:: hide

      | :sl:`Hide the window`
      | :sg:`hide() -> None`

      .. ## Window.hide ##
   
   .. method:: show

      | :sl:`Show the window`
      | :sg:`show() -> None`

      .. ## Window.show ##
   
   .. method:: restore

      | :sl:`Restore the size and position of a minimized or maximized window`
      | :sg:`restore() -> None`

      .. ## Window.restore ##
   
   .. method:: maximize

      | :sl:`Maximize the window`
      | :sg:`maximize() -> None`

      .. ## Window.maximize ##
   
   .. method:: minimize

      | :sl:`Minimize the window`
      | :sg:`minimize() -> None`

      .. ## Window.minimize ##
      
   .. method:: set_modal_for

      | :sl:`Set the window as a modal for a parent window`
      | :sg:`set_modal_for(parent) -> None`

      :param Window parent: The parent window.
      
      This function is only supported on X11.

      .. ## Window.set_modal_for ##
   
   .. method:: set_icon

      | :sl:`Set the icon for the window`
      | :sg:`set_icon(icon) -> None`

      :param Surface surface: A Surface to use as the icon.

      .. ## Window.set_icon ##

   .. ## pygame.window.Window ##