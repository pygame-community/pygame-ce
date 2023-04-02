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

   .. ## pygame.window.Window ##