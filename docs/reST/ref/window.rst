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

   | :sl:`docs_needed`
   | :sg:`Window(title='pygame window', size=(640, 480), position=WINDOWPOS_UNDEFINED, **flags)`

   .. classmethod:: from_display_module
   
      | :sl:`docs_needed`
      | :sg:`from_display_module() -> Window`

      .. ## Window.from_display_module ##
   
   .. classmethod:: from_existing_window
   
      | :sl:`docs_needed`
      | :sg:`from_existing_window(hwnd) -> Window`

      .. ## Window.from_existing_window ##

   .. method:: destroy

      | :sl:`docs_needed`
      | :sg:`destroy() -> None`

      .. ## Window.destroy ##

   .. method:: set_windowed

      | :sl:`docs_needed`
      | :sg:`set_windowed() -> None`

      .. ## Window.set_windowed ##

   .. method:: set_fullscreen

      | :sl:`docs_needed`
      | :sg:`set_fullscreen(desktop=False) -> None`

      .. ## Window.set_fullscreen ##
   
   .. method:: focus

      | :sl:`docs_needed`
      | :sg:`focus(input_only=False) -> None`

      .. ## Window.focus ##
   
   .. method:: hide

      | :sl:`docs_needed`
      | :sg:`hide() -> None`

      .. ## Window.hide ##
   
   .. method:: show

      | :sl:`docs_needed`
      | :sg:`show() -> None`

      .. ## Window.show ##
   
   .. method:: restore

      | :sl:`docs_needed`
      | :sg:`restore() -> None`

      .. ## Window.restore ##
   
   .. method:: maximize

      | :sl:`docs_needed`
      | :sg:`maximize() -> None`

      .. ## Window.maximize ##
   
   .. method:: minimize

      | :sl:`docs_needed`
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

      | :sl:`docs_needed`
      | :sg:`set_modal_for(parent) -> None`

      .. ## Window.set_modal_for ##
   
   .. method:: update_from_surface

      | :sl:`docs_needed`
      | :sg:`update_from_surface(*rects) -> None`

      .. ## Window.update_from_surface ##

   .. method:: set_grab

      | :sl:`docs_needed`
      | :sg:`set_grab(enable) -> None`

      .. ## Window.set_grab ##
   
   .. method:: get_grab

      | :sl:`docs_needed`
      | :sg:`get_grab() -> bool`

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

      | :sl:`docs_needed`
      | :sg:`set_title(title) -> None`

      .. ## Window.set_title ##
   
   .. method:: get_title

      | :sl:`docs_needed`
      | :sg:`get_title() -> str`

      .. ## Window.get_title ##
   
   .. method:: set_resizable

      | :sl:`docs_needed`
      | :sg:`set_resizable(enable) -> None`

      .. ## Window.set_resizable ##
   
   .. method:: get_resizable

      | :sl:`docs_needed`
      | :sg:`get_resizable() -> bool`

      .. ## Window.get_resizable ##
   
   .. method:: set_borderless

      | :sl:`docs_needed`
      | :sg:`set_borderless(enable) -> None`

      .. ## Window.set_borderless ##
   
   .. method:: get_borderless

      | :sl:`docs_needed`
      | :sg:`get_borderless() -> bool`

      .. ## Window.get_borderless ##
   
   .. method:: set_size

      | :sl:`docs_needed`
      | :sg:`set_size((width, height)) -> None`

      .. ## Window.set_size ##
   
   .. method:: get_size

      | :sl:`docs_needed`
      | :sg:`get_size() -> (width, height)`

      .. ## Window.get_size ##
   
   .. method:: set_position

      | :sl:`docs_needed`
      | :sg:`set_position((x, y)) -> None`

      .. ## Window.set_position ##
   
   .. method:: get_position

      | :sl:`docs_needed`
      | :sg:`get_position() -> (x, y)`

      .. ## Window.get_position ##
   
   .. method:: set_opacity

      | :sl:`docs_needed`
      | :sg:`set_opacity(opacity) -> None`

      .. ## Window.set_opacity ##
   
   .. method:: get_opacity

      | :sl:`docs_needed`
      | :sg:`get_opacity() -> float`

      .. ## Window.get_opacity ##
   
   .. method:: set_icon

      | :sl:`docs_needed`
      | :sg:`set_icon(icon) -> None`

      .. ## Window.set_icon ##
   
   .. method:: get_display_index

      | :sl:`docs_needed`
      | :sg:`get_display_index() -> int`

      .. ## Window.get_display_index ##
   
   .. method:: get_surface

      | :sl:`docs_needed`
      | :sg:`get_surface() -> Surface`

      .. ## Window.get_surface ##
   
   .. method:: get_window_id

      | :sl:`docs_needed`
      | :sg:`get_window_id() -> int`

      .. ## Window.get_window_id ##

   .. method:: get_wm_info

      | :sl:`docs_needed`
      | :sg:`get_wm_info() -> dict`

      .. ## Window.get_wm_info ##

   .. ## pygame.window.Window ##