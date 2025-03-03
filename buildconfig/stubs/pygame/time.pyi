"""Pygame module for monitoring time.

Provides utilities for monitoring time, delaying time, and maintaining a
constant frame rate.
Times in pygame-ce are represented in milliseconds (1/1000 of a second).
"""

from typing import Union, final

from pygame.event import Event

def get_ticks() -> int:
    """Get the time in milliseconds.

    Return the number of milliseconds since ``pygame.init()`` was called. Before
    pygame is initialized this will always be 0.
    """

def wait(milliseconds: int, /) -> int:
    """Pause the program for an amount of time.

    Will pause for a given number of milliseconds. This function sleeps the
    process to share the processor with other programs. A program that waits for
    even a few milliseconds will consume very little processor time. It is
    slightly less accurate than the ``pygame.time.delay()`` function.

    This returns the actual number of milliseconds used.
    """

def delay(milliseconds: int, /) -> int:
    """Pause the program for an amount of time.

    Will pause for a given number of milliseconds. This function will use the
    processor (rather than sleeping) in order to make the delay more accurate
    than ``pygame.time.wait()``.

    This returns the actual number of milliseconds used.
    """

def set_timer(event: Union[int, Event], millis: int, loops: int = 0) -> None:
    """Repeatedly create an event on the event queue.

    Set an event to appear on the event queue every given number of milliseconds.
    The first event will not appear until the amount of time has passed.

    The ``event`` attribute can be a ``pygame.event.Event`` object or an integer
    type that denotes an event.

    ``loops`` is an integer that denotes the number of events posted. If 0 (default)
    then the events will keep getting posted, unless explicitly stopped.

    To disable the timer for such an event, call the function again with the same
    event argument with ``millis`` argument set to 0.

    It is also worth mentioning that a particular event type can only be put on a
    timer once. In other words, there cannot be two timers for the same event type.
    Setting an event timer for a particular event discards the old one for that
    event type.

    When this function is called with an ``Event`` object, the event(s) received
    on the event queue will be a shallow copy; the dict attribute of the event
    object passed as an argument and the dict attributes of the event objects
    received on timer will be references to the same dict object in memory.
    Modifications on one dict can affect another, use deepcopy operations on the
    dict object if you don't want this behaviour.
    However, calling this function with an integer event type would place event objects
    on the queue that don't have a common dict reference.

    ``loops`` replaces the ``once`` argument, and this does not break backward
    compatibility.

    .. versionaddedold:: 2.0.0.dev3 once argument added.
    .. versionchangedold:: 2.0.1 event argument supports ``pygame.event.Event`` object
    .. versionaddedold:: 2.0.1 added loops argument to replace once argument
    """

@final
class Clock:
    """Create an object to help track time.

    Creates a new Clock object that can be used to track an amount of time. The
    clock also provides several functions to help control a game's framerate.

    .. versionchanged:: 2.1.4  This class is also available through the ``pygame.Clock``
       alias.
    """

    def __new__(cls) -> Clock: ...
    def tick(self, framerate: float = 0, /) -> int:
        """Update the clock.

        This method should be called once per frame. It will compute how many
        milliseconds have passed since the previous call.

        If you pass the optional framerate argument the function will delay to
        keep the game running slower than the given ticks per second. This can be
        used to help limit the runtime speed of a game. By calling
        ``Clock.tick(40)`` once per frame, the program will never run at more
        than 40 frames per second.

        Note that this function uses SDL_Delay function which is not accurate on
        every platform, but does not use much CPU. Use tick_busy_loop if you want
        an accurate timer, and don't mind chewing CPU.
        """

    def tick_busy_loop(self, framerate: float = 0, /) -> int:
        """Update the clock.

        This method should be called once per frame. It will compute how many
        milliseconds have passed since the previous call.

        If you pass the optional framerate argument the function will delay to
        keep the game running slower than the given ticks per second. This can be
        used to help limit the runtime speed of a game. By calling
        ``Clock.tick_busy_loop(40)`` once per frame, the program will never run at
        more than 40 frames per second.

        Note that this function uses :func:`pygame.time.delay`, which uses lots
        of CPU in a busy loop to make sure that timing is more accurate.

        .. versionaddedold:: 1.8
        """

    def get_time(self) -> int:
        """Time used in the previous tick.

        The number of milliseconds that passed between the previous two calls to
        ``Clock.tick()``.
        """

    def get_rawtime(self) -> int:
        """Actual time used in the previous tick.

        Similar to ``Clock.get_time()``, but does not include any time used
        while ``Clock.tick()`` was delaying to limit the framerate.
        """

    def get_fps(self) -> float:
        """Compute the clock framerate.

        Compute your game's framerate (in frames per second). It is computed by
        averaging the last ten calls to ``Clock.tick()``.
        """
