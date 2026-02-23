"""Pygame module to work with the mouse.

The mouse functions can be used to get the current state of the mouse device.
These functions can also alter the system cursor for the mouse.

When the display mode is set, the event queue will start receiving mouse
events. The mouse buttons generate ``pygame.MOUSEBUTTONDOWN`` and
``pygame.MOUSEBUTTONUP`` events when they are pressed and released. These
events contain a button attribute representing which button was pressed. The
mouse wheel will generate ``pygame.MOUSEBUTTONDOWN`` and
``pygame.MOUSEBUTTONUP`` events when rolled. The button will be set to 4
when the wheel is rolled up, and to button 5 when the wheel is rolled down.
Whenever the mouse is moved it generates a ``pygame.MOUSEMOTION`` event. The
mouse movement is broken into small and accurate motion events. As the mouse
is moving many motion events will be placed on the queue. Mouse motion events
that are not properly cleaned from the event queue are the primary reason the
event queue fills up.

If the mouse cursor is hidden, and input is grabbed to the current display the
mouse will enter a virtual input mode, where the relative movements of the
mouse will never be stopped by the borders of the screen. See the functions
``pygame.mouse.set_visible()`` and ``pygame.event.set_grab()`` to get this
configured.

**Mouse Wheel Behavior in pygame 2**

There is proper functionality for mouse wheel behaviour with pygame 2 supporting
``pygame.MOUSEWHEEL`` events.  The new events support horizontal and vertical
scroll movements, with signed integer values representing the amount scrolled
(``x`` and ``y``), as well as ``flipped`` direction (the set positive and
negative values for each axis is flipped). Read more about SDL2
input-related changes here `<https://wiki.libsdl.org/MigrationGuide#input>`_

In pygame 2, the mouse wheel functionality can be used by listening for the
``pygame.MOUSEWHEEL`` type of an event (Bear in mind they still emit
``pygame.MOUSEBUTTONDOWN`` events like in pygame 1.x, as well).
When this event is triggered, a developer can access the appropriate ``Event`` object
with ``pygame.event.get()``. The object can be used to access data about the mouse
scroll, such as ``which`` (it will tell you what exact mouse device trigger the event).

.. code-block:: python
   :caption: Code example of mouse scroll (tested on 2.0.0.dev7)
   :name: test.py

   # Taken from husano896's PR thread (slightly modified)
   import pygame
   from pygame.locals import *
   pygame.init()
   screen = pygame.display.set_mode((640, 480))
   clock = pygame.time.Clock()

   def main():
       while True:
           for event in pygame.event.get():
               if event.type == QUIT:
                   pygame.quit()
                   return
               elif event.type == MOUSEWHEEL:
                   print(event)
                   print(event.x, event.y)
                   print(event.flipped)
                   print(event.which)
                   # can access properties with
                   # proper notation(ex: event.y)
           clock.tick(60)

   # Execute game:
   main()
"""

from typing import Any, Literal, overload

from pygame.cursors import Cursor
from pygame.surface import Surface
from pygame.typing import IntPoint, Point, SequenceLike
from typing_extensions import deprecated  # added in 3.13

@overload
def get_pressed(
    num_buttons: Literal[3] = 3, desktop: bool = False
) -> tuple[bool, bool, bool]: ...
@overload
def get_pressed(
    num_buttons: Literal[5], desktop: bool = False
) -> tuple[bool, bool, bool, bool, bool]: ...
def get_pressed(*args, **kwargs) -> Any:  # type: ignore
    """Get the state of the mouse buttons.

    Returns a sequence of booleans representing the state of all the mouse
    buttons. A true value means the mouse is currently being pressed at the time
    of the call.

    To get all of the mouse events it is better to use either
    ``pygame.event.wait()`` or ``pygame.event.get()`` and check all of those
    events to see if they are ``MOUSEBUTTONDOWN``, ``MOUSEBUTTONUP``, or
    ``MOUSEMOTION``. Remember to call ``pygame.event.get()`` or ``pygame.event.pump()``
    before this function, otherwise it will not work as expected.

    To support five button mice, an optional parameter ``num_buttons`` has been
    added in pygame 2. When this is set to ``5``, ``button4`` and ``button5``
    are added to the returned tuple. Only ``3`` and ``5`` are valid values
    for this parameter.

    If the ``desktop`` argument is ``True`` the mouse state will be correct even
    if the window has no focus. In addition since it queries the OS it does not depend
    on the last event pump while being slightly slower.

    .. note:: On ``X11`` some X servers use middle button emulation. When you
       click both buttons ``1`` and ``3`` at the same time a ``2`` button event
       can be emitted.

    .. warning:: Due to design constraints it is impossible to retrieve the desktop
       mouse state on Wayland. The normal mouse state is returned instead.

    .. versionchangedold:: 2.0.0 ``num_buttons`` argument added

    .. versionchanged:: 2.5.2 Added the ``desktop`` argument
    """

def get_just_pressed() -> tuple[bool, bool, bool, bool, bool]:
    """Get the most recently pressed buttons.

    Very similar to :func:`pygame.mouse.get_pressed()`, returning a tuple
    of length 5 with the important difference that the buttons are
    True only in the frame they start being pressed. This can be convenient
    for checking the buttons pressed "this frame", but for more precise results
    and correct ordering prefer using the ``pygame.MOUSEBUTTONDOWN`` event.

    The result of this function is updated when new events are processed,
    e.g. in :func:`pygame.event.get()` or :func:`pygame.event.pump()`.

    .. seealso:: :func:`pygame.mouse.get_just_released()`

    ::

       if pygame.mouse.get_just_pressed()[0]:
          print("LMB just pressed")

    .. versionadded:: 2.5.0
    """

def get_just_released() -> tuple[bool, bool, bool, bool, bool]:
    """Get the most recently released buttons.

    Similar to :func:`pygame.mouse.get_pressed()`, returning a tuple
    of length 5 with the important difference that the buttons are
    True only in the frame they stop being pressed. This can be convenient
    for checking the buttons released "this frame", but for more precise results
    and correct ordering prefer using the ``pygame.MOUSEBUTTONUP`` event.

    The result of this function is updated when new events are processed,
    e.g. in :func:`pygame.event.get()` or :func:`pygame.event.pump()`.

    .. seealso:: :func:`pygame.mouse.get_just_pressed()`

    ::

       if pygame.mouse.get_just_released()[0]:
          print("LMB just released")

    .. versionadded:: 2.5.0
    """

def get_pos(desktop: bool = False) -> tuple[int, int]:
    """Get the mouse cursor position.

    By default returns the ``x`` and ``y`` position of the mouse cursor. The position
    is relative to the top-left corner of the display. The cursor position can be
    located outside of the display window, but is always constrained to the screen.

    If the ``desktop`` argument is ``True``, the position will be instead relative to the
    top-left corner of the primary monitor. The position might be negative or exceed
    the desktop bounds if multiple monitors are present.

    .. warning:: Due to design constraints it is impossible to retrieve the desktop
       mouse state on Wayland. The relative mouse position is returned instead.

    .. versionchanged:: 2.5.2 Added the ``desktop`` argument
    """

def get_rel() -> tuple[int, int]:
    """Get the amount of mouse movement.

    Returns the amount of movement in ``x`` and ``y`` since the previous call to
    this function. The relative movement of the mouse cursor is constrained to
    the edges of the screen, but see the virtual input mouse mode for a way
    around this. Virtual input mode is described at the top of the page.
    """

@overload
def set_pos(pos: Point, /) -> None: ...
@overload
def set_pos(x: float, y: float, /) -> None: ...
def set_pos(*args) -> None:  # type: ignore
    """Set the mouse cursor position.

    Set the current mouse position to arguments given. If the mouse cursor is
    visible it will jump to the new coordinates. Moving the mouse will generate
    a new ``pygame.MOUSEMOTION`` event.
    """

def set_visible(value: bool, /) -> int:
    """Hide or show the mouse cursor.

    If the bool argument is true, the mouse cursor will be visible. This will
    return the previous visible state of the cursor.
    """

def get_visible() -> bool:
    """Get the current visibility state of the mouse cursor.

    Get the current visibility state of the mouse cursor. ``True`` if the mouse is
    visible, ``False`` otherwise.

    .. versionaddedold:: 2.0.0
    """

def get_focused() -> bool:
    """Check if the display is receiving mouse input.

    Returns true when pygame is receiving mouse input events (or, in windowing
    terminology, is "active" or has the "focus").

    This method is most useful when working in a window. By contrast, in
    full-screen mode, this method always returns true.

    Note: under ``MS`` Windows, the window that has the mouse focus also has the
    keyboard focus. But under X-Windows, one window can receive mouse events and
    another receive keyboard events. ``pygame.mouse.get_focused()`` indicates
    whether the pygame window receives mouse events.
    """

@overload
def set_cursor(cursor: Cursor) -> None: ...
@overload
def set_cursor(
    size: IntPoint,
    hotspot: IntPoint,
    xormasks: SequenceLike[int],
    andmasks: SequenceLike[int],
) -> None: ...
@overload
def set_cursor(hotspot: IntPoint, surface: Surface) -> None: ...
@overload
def set_cursor(constant: int) -> None: ...
def set_cursor(*args, **kwargs) -> None:  # type: ignore
    """Set the mouse cursor to a new cursor.

    Set the mouse cursor to something new. This function accepts either an explicit
    ``Cursor`` object or arguments to create a ``Cursor`` object.

    See :class:`pygame.cursors.Cursor` for help creating cursors and for examples.

    .. versionchangedold:: 2.0.1
    """

def get_cursor() -> Cursor:
    """Get the current mouse cursor.

    Get the information about the mouse system cursor. The return value contains
    the same data as the arguments passed into :func:`pygame.mouse.set_cursor()`.

    .. note:: Code that unpacked a get_cursor() call into
              ``size, hotspot, xormasks, andmasks`` will still work,
              assuming the call returns an old school type cursor.

    .. versionchangedold:: 2.0.1
    """

@deprecated("since 2.2.0. Use `pygame.mouse.set_cursor` instead")
def set_system_cursor(cursor: int, /) -> None: ...
def get_relative_mode() -> bool:
    """Query whether relative mouse mode is enabled.

    Query whether relative mouse mode is enabled.

    .. versionadded:: 2.4.0
    """

def set_relative_mode(enable: bool, /) -> None:
    """Set relative mouse mode.

    Sets the relative mouse mode state.
    While the mouse is in relative mode, the cursor is hidden,
    the mouse position is constrained to the window, and pygame
    will report continuous relative mouse motion even if the
    mouse is at the edge of the window.

    *This function will flush any pending mouse motion."*

    Calling :func:`pygame.mouse.set_visible` with argument
    ``True`` will exit relative mouse mode.

    .. versionadded:: 2.4.0
    .. versionchanged:: 2.5.6 calling this function before calling
        :func:`pygame.display.set_mode` is deprecated and may error in the future.
    """
