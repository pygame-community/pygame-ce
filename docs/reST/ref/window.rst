.. include:: common.txt

:mod:`pygame.window`
=====================

.. module:: pygame.window
   :synopsis: pygame module to control windows

| :sl:`pygame module to control windows`

.. function:: get_windows

   | :sl:`docs_needed`
   | :sg:`get_windows() -> Tuple[Window, ...]`

   .. ## pygame.window.get_windows ##

.. function:: get_grabbed_window

   | :sl:`docs_needed`
   | :sg:`get_grabbed_window() -> Optional[Window]`

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
   :param bool vulkan: Create a window with support for Metal.
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
   
   .. classmethod:: from_existing_window
   
      | :sl:`Create a Window object and embed the window to an existing window`
      | :sg:`from_existing_window(hwnd) -> Window`

      :param int hwnd: The handle/windowID of the existing window.

      .. ## Window.from_existing_window ##

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
   
   .. method:: flash

      | :sl:`docs_needed`
      | :sg:`flash(briefly=False) -> None`

      .. ## Window.flash ##
   
   .. method:: flash_cancel

      | :sl:`docs_needed`
      | :sg:`flash_cancel() -> None`

      .. ## Window.flash_cancel ##
      
   .. method:: set_modal_for

      | :sl:`Set the window as a modal for a parent window`
      | :sg:`set_modal_for(parent) -> None`

      :param Window parent: The parent window.
      
      This function is only supported on X11.

      .. ## Window.set_modal_for ##
   
   .. method:: update_from_surface

      | :sl:`docs_needed`
      | :sg:`update_from_surface(*rects) -> None`

      .. ## Window.update_from_surface ##

   .. method:: set_grab

      | :sl:`Set the window's input grab state`
      | :sg:`set_grab(enable) -> None`

      :param bool grabbed: The new input grab state.

      When input is grabbed, the mouse is confined to the window.
      If the caller enables a grab while another window is currently grabbed,
      the other window loses its grab in favor of the caller's window.

      .. ## Window.set_grab ##
   
   .. method:: get_grab

      | :sl:`Get the window's input grab state`
      | :sg:`get_grab() -> bool`

      Get the window's input grab state (whether the mouse is confined to the
      window).

      .. ## Window.get_grab ##
   
   .. method:: set_always_on_top

      | :sl:`docs_needed`
      | :sg:`set_always_on_top(enable) -> None`

      .. ## Window.set_always_on_top ##
   
   .. method:: get_always_on_top

      | :sl:`docs_needed`
      | :sg:`get_always_on_top() -> bool`

      .. ## Window.get_always_on_top ##

   .. method:: set_title

      | :sl:`Set the window title`
      | :sg:`set_title(title) -> None`

      :param str title: The new window title.

      .. ## Window.set_title ##
   
   .. method:: get_title

      | :sl:`Get the window title`
      | :sg:`get_title() -> str`

      Get the window title, or an empty string if there is none.

      .. ## Window.get_title ##
   
   .. method:: set_resizable

      | :sl:`Set whether the window is resizable`
      | :sg:`set_resizable(enable) -> None`

      .. ## Window.set_resizable ##
   
   .. method:: get_resizable

      | :sl:`Get whether the window is resizable`
      | :sg:`get_resizable() -> bool`

      .. ## Window.get_resizable ##
   
   .. method:: set_borderless

      | :sl:`Set whether the window is borderless`
      | :sg:`set_borderless(enable) -> None`

      .. ## Window.set_borderless ##
   
   .. method:: get_borderless

      | :sl:`Get whether the window is borderless`
      | :sg:`get_borderless() -> bool`

      .. ## Window.get_borderless ##
   
   .. method:: set_size

      | :sl:`Set the window size`
      | :sg:`set_size((width, height)) -> None`

      :param (int, int) size: The new window size.

      .. ## Window.set_size ##
   
   .. method:: get_size

      | :sl:`Get the window size`
      | :sg:`get_size() -> (width, height)`

      .. ## Window.get_size ##
   
   .. method:: set_position

      | :sl:`Set the window's screen position`
      | :sg:`set_position((x, y)) -> None`

      :param (int, int) or int position: The coordinates as an x, y tuple, or
         as ``pygame.WINDOWPOS_CENTERED`` to center the window.

      .. ## Window.set_position ##
   
   .. method:: get_position

      | :sl:`Get the window's screen position`
      | :sg:`get_position() -> (x, y)`

      .. ## Window.get_position ##
   
   .. method:: set_opacity

      | :sl:`Set the window opacity`
      | :sg:`set_opacity(opacity) -> None`

      :param float opacity: The new opacity value between 0.0
         (fully transparent) and 1.0 (fully opaque).

      .. ## Window.set_opacity ##
   
   .. method:: get_opacity

      | :sl:`Get the window opacity`
      | :sg:`get_opacity() -> float`

      Get the window opacity, a floating point value between 0.0 (fully transparent)
      and 1.0 (fully opaque).

      .. ## Window.get_opacity ##
   
   .. method:: set_icon

      | :sl:`Set the icon for the window`
      | :sg:`set_icon(icon) -> None`

      :param Surface surface: A Surface to use as the icon.

      .. ## Window.set_icon ##
   
   .. method:: get_display_index

      | :sl:`Get the index of the display that owns the window`
      | :sg:`get_display_index() -> int`

      .. ## Window.get_display_index ##
   
   .. method:: get_surface

      | :sl:`docs_needed`
      | :sg:`get_surface() -> Surface`

      .. ## Window.get_surface ##
   
   .. method:: get_window_id

      | :sl:`Get the unique window ID`
      | :sg:`get_window_id() -> int`

      .. ## Window.get_window_id ##

   .. method:: get_foreign

      | :sl:`docs_needed`
      | :sg:`get_foreign() -> bool`

      .. ## Window.get_foreign ##

   .. method:: get_wm_info

      | :sl:`docs_needed`
      | :sg:`get_wm_info() -> dict`

      .. ## Window.get_wm_info ##

   .. ## pygame.window.Window ##