"""Pygame module to control the display window and screen.

This module offers control over the pygame display. Pygame has a single display
Surface that is either contained in a window or runs full screen. Once you
create the display you treat it as a regular Surface. Changes are not
immediately visible onscreen; you must choose one of the two flipping functions
to update the actual display.

The origin of the display, where x = 0 and y = 0, is the top left of the
screen. Both axes increase positively towards the bottom right of the screen.

The pygame display can actually be initialized in one of several modes. By
default, the display is a basic software driven framebuffer. You can request
special modules like automatic scaling or OpenGL support. These are
controlled by flags passed to ``pygame.display.set_mode()``.

Pygame can only have a single display active at any time. Creating a new one
with ``pygame.display.set_mode()`` will close the previous display. To detect
the number and size of attached screens, you can use
``pygame.display.get_desktop_sizes`` and then select appropriate window size
and display index to pass to ``pygame.display.set_mode()``.

For backward compatibility ``pygame.display`` allows precise control over
the pixel format or display resolutions. This used to be necessary with old
graphics cards and CRT screens, but is usually not needed any more. Use the
functions ``pygame.display.mode_ok()``, ``pygame.display.list_modes()``, and
``pygame.display.Info()`` to query detailed information about the display.

Once the display Surface is created, the functions from this module affect the
single existing display. The Surface becomes invalid if the module is
uninitialized. If a new display mode is set, the existing Surface will
automatically switch to operate on the new display.

When the display mode is set, several events are placed on the pygame event
queue. ``pygame.QUIT`` is sent when the user has requested the program to
shut down. The window will receive ``pygame.ACTIVEEVENT`` events as the display
gains and loses input focus. If the display is set with the
``pygame.RESIZABLE`` flag, ``pygame.VIDEORESIZE`` events will be sent when the
user adjusts the window dimensions. Hardware displays that draw direct to the
screen will get ``pygame.VIDEOEXPOSE`` events when portions of the window must
be redrawn.

A new windowevent API was introduced in pygame 2.0.1. Check event module docs
for more information on that

Some display environments have an option for automatically stretching all
windows. When this option is enabled, this automatic stretching distorts the
appearance of the pygame window. In the pygame examples directory, there is
example code (prevent_display_stretching.py) which shows how to disable this
automatic stretching of the pygame display on Microsoft Windows (Vista or newer
required).
"""

from collections.abc import Iterable
from typing import Literal, Optional, Union, overload

from pygame._sdl2 import Window
from pygame.constants import FULLSCREEN
from pygame.surface import Surface
from pygame.typing import (
    ColorLike,
    IntPoint,
    Point,
    RectLike,
    SequenceLike,
)
from typing_extensions import deprecated  # added in 3.13

class _VidInfo:
    @property
    def hw(self) -> int: ...
    @property
    def wm(self) -> int: ...
    @property
    def video_mem(self) -> int: ...
    @property
    def bitsize(self) -> int: ...
    @property
    def bytesize(self) -> int: ...
    @property
    def masks(self) -> tuple[int, int, int, int]: ...
    @property
    def shifts(self) -> tuple[int, int, int, int]: ...
    @property
    def losses(self) -> tuple[int, int, int, int]: ...
    @property
    def blit_hw(self) -> int: ...
    @property
    def blit_hw_CC(self) -> int: ...
    @property
    def blit_hw_A(self) -> int: ...
    @property
    def blit_sw(self) -> int: ...
    @property
    def blit_sw_CC(self) -> int: ...
    @property
    def blit_sw_A(self) -> int: ...
    @property
    def current_h(self) -> int: ...
    @property
    def current_w(self) -> int: ...
    @property
    def pixel_format(self) -> str: ...

def init() -> None:
    """Initialize the display module.

    Initializes the pygame display module. The display module cannot do anything
    until it is initialized. This is usually handled for you automatically when
    you call the higher level ``pygame.init()``.

    Pygame will select from one of several internal display backends when it is
    initialized. The display mode will be chosen depending on the platform and
    permissions of current user. Before the display module is initialized the
    environment variable ``SDL_VIDEODRIVER`` can be set to control which backend
    is used. The systems with multiple choices are listed here.

    ::

        Windows : windib, directx
        Unix    : x11, dga, fbcon, directfb, ggi, vgl, svgalib, aalib, wayland

    :note: On wayland desktops, pygame-ce may choose to use the X11 video driver to run on Xwayland.
        This behaviour is determined by the SDL library and might change in the future, so it's suggested
        to account for this and not rely on the default behavior. The Wayland video driver can be forced
        by setting the ``SDL_VIDEODRIVER`` environment variable to ``"wayland"``

    On some platforms it is possible to embed the pygame display into an already
    existing window. To do this, the environment variable ``SDL_WINDOWID`` must
    be set to a string containing the window id or handle. The environment
    variable is checked when the pygame display is initialized. Be aware that
    there can be many strange side effects when running in an embedded display.

    It is harmless to call this more than once, repeated calls have no effect.

    .. versionchanged:: 2.5.0 the manylinux wheels distributed by us now support the ``wayland`` videodriver

    """

def quit() -> None:
    """Uninitialize the display module.

    This will shut down the entire display module. This means any active
    displays will be closed. This will also be handled automatically when the
    program exits.

    It is harmless to call this more than once, repeated calls have no effect.
    """

def get_init() -> bool:
    """Returns True if the display module has been initialized.

    Returns True if the :mod:`pygame.display` module is currently initialized.
    """

def set_mode(
    size: Point = (0, 0),
    flags: int = 0,
    depth: int = 0,
    display: int = 0,
    vsync: int = 0,
) -> Surface:
    """Initialize a window or screen for display.

    This will create a window or display output and return a display Surface.
    The arguments passed in are requests for a display type. The actual created
    display will be the best possible match supported by the system.

    Note that calling this function implicitly initializes ``pygame.display``, if
    it was not initialized before.

    The size argument is a pair of numbers representing the width and
    height. The flags argument is a collection of additional options. The depth
    argument represents the number of bits to use for color.

    The Surface that gets returned can be drawn to like a regular Surface but
    changes will eventually be seen on the monitor.

    If no size is passed or is set to ``(0, 0)``, the created Surface will have
    the same size as the current screen resolution. If only the width or height
    are set to ``0``, the Surface will have the same width or height as the
    screen resolution.

    Since pygame 2, the depth argument is ignored, in favour of the best
    and fastest one. It also raises a deprecation warning since pygame-ce
    2.4.0 if the passed in depth is not 0 or the one pygame selects.

    When requesting fullscreen display modes, sometimes an exact match for the
    requested size cannot be made. In these situations pygame will select
    the closest compatible match. The returned surface will still always match
    the requested size.

    On high resolution displays(4k, 1080p) and tiny graphics games (640x480)
    show up very small so that they are unplayable. SCALED scales up the window
    for you. The game thinks it's a 640x480 window, but really it can be bigger.
    Mouse events are scaled for you, so your game doesn't need to do it. Note
    that SCALED is considered an experimental API and may change in future
    releases.

    The flags argument controls which type of display you want. There are
    several to choose from, and you can even combine multiple types using the
    bitwise or operator, (the pipe "|" character). Here are the display
    flags you will want to choose from:

    ::

        pygame.FULLSCREEN    create a fullscreen display
        pygame.DOUBLEBUF     only applicable with OPENGL
        pygame.HWSURFACE     (obsolete in pygame 2) hardware accelerated, only in FULLSCREEN
        pygame.OPENGL        create an OpenGL-renderable display
        pygame.RESIZABLE     display window should be sizeable
        pygame.NOFRAME       display window will have no border or controls
        pygame.SCALED        resolution depends on desktop size and scale graphics
        pygame.SHOWN         window is opened in visible mode (default)
        pygame.HIDDEN        window is opened in hidden mode


    .. versionaddedold:: 2.0.0 ``SCALED``, ``SHOWN`` and ``HIDDEN``

    .. versionaddedold:: 2.0.0 ``vsync`` parameter

    By setting the ``vsync`` parameter to ``1``, it is possible to get a display
    with vertical sync at a constant frame rate determined by the monitor and
    graphics drivers. Subsequent calls to :func:`pygame.display.flip()` or
    :func:`pygame.display.update()` will block (i.e. *wait*) until the screen
    has refreshed, in order to prevent "screen tearing"
    <https://en.wikipedia.org/wiki/Screen_tearing>.

    Be careful when using this feature together with ``pygame.time.Clock`` or
    :func:`pygame.time.delay()`, as multiple forms of waiting and frame rate
    limiting may interact to cause skipped frames.

    The request only works when graphics acceleration is available on the
    system. The exact behaviour depends on the hardware and driver
    configuration. When  ``vsync`` is requested, but unavailable,
    ``set_mode()`` may raise an exception.

    Setting the ``vsync`` parameter to ``-1`` in conjunction with  ``OPENGL``
    will request the OpenGL-specific feature "adaptive vsync" <https://www.khronos.org/opengl/wiki/Swap_Interval#Adaptive_Vsync>.

    Here is an example usage of a call
    to ``set_mode()`` that may give you a display with vsync:

    ::

        flags = pygame.OPENGL | pygame.FULLSCREEN
        try:
            window_surface = pygame.display.set_mode((1920, 1080), flags, vsync=1)
            vsync_success=True
        except pygame.error:
            window_surface = pygame.display.set_mode((1920, 1080), flags)
            vsync_success=False

    .. versionaddedold:: 2.0.0 ``vsync`` parameter

    .. versionchanged:: 2.2.0 passing ``vsync`` can raise an exception

    .. versionchanged:: 2.2.0 explicit request for "adaptive vsync"

    .. versionchanged:: 2.2.0 ``vsync=1`` does not require ``SCALED`` or ``OPENGL``

    .. deprecated:: 2.4.0 The depth argument is ignored, and will be set to the optimal value

    .. versionchanged:: 2.5.0 No longer emits warning when running on xwayland, see :func:`pygame.display.init` for details on running on wayland directly

    Basic example:

    ::

        # Open a window on the screen
        screen_width=700
        screen_height=400
        screen=pygame.display.set_mode([screen_width, screen_height])

    The display index ``0`` means the default display is used. If no display
    index argument is provided, the default display can be overridden with an
    environment variable.


    .. versionchangedold:: 1.9.5 ``display`` argument added

    .. versionchanged:: 2.1.3
        pygame now ensures that subsequent calls to this function clears the
        window to black. On older versions, this was an implementation detail
        on the major platforms this function was tested with.
    """

def get_surface() -> Optional[Surface]:
    """Get a reference to the currently set display surface.

    Return a reference to the currently set display Surface. If no display mode
    has been set this will return None.
    """

def flip() -> None:
    """Update the full display Surface to the screen.

    This will update the contents of the entire display.

    When using an ``pygame.OPENGL`` display mode this will perform a gl buffer
    swap.
    """

@overload
def update() -> None: ...
@overload
def update(rectangle: Optional[RectLike], /) -> None: ...
@overload
def update(rectangles: Iterable[Optional[RectLike]], /) -> None: ...
@overload
def update(x: float, y: float, w: float, h: float, /) -> None: ...
@overload
def update(xy: Point, wh: Point, /) -> None: ...
def update(*args):  # type: ignore
    """Update all, or a portion, of the display. For non-OpenGL displays.

    For non OpenGL display Surfaces, this function is very similar to
    ``pygame.display.flip()`` with an optional parameter that allows only
    portions of the display surface to be updated, instead of the entire area.
    If no argument is passed it updates the entire Surface area like
    ``pygame.display.flip()``.

    .. note:: calling ``display.update(None)`` means no part of the window is
        updated. Whereas ``display.update()`` means the whole window is
        updated.

    You can pass the function a single rectangle, or an iterable of rectangles.
    Generally you do not want to pass an iterable of rectangles as there is a
    performance cost per rectangle passed to the function. On modern hardware,
    after a very small number of rectangles passed in, the per-rectangle cost
    will exceed the saving of updating less pixels. In most applications it is
    simply more efficient to update the entire display surface at once, it also
    means  you do not need to keep track of a list of rectangles for each call
    to update.

    If passing an iterable of rectangles it is safe to include None
    values in the list, which will be skipped.

    This call cannot be used on ``pygame.OPENGL`` displays and will generate an
    exception.

    .. versionchanged:: 2.5.1 Added support for passing an iterable, previously only sequence was allowed
    """

def get_driver() -> str:
    """Get the name of the pygame display backend.

    Pygame chooses one of many available display backends when it is
    initialized. This returns the internal name used for the display backend.
    This can be used to provide limited information about what display
    capabilities might be accelerated. See the ``SDL_VIDEODRIVER`` flags in
    ``pygame.display.init()`` to see some of the common options.
    """

def Info() -> _VidInfo:
    """Create a video display information object.

    Creates a simple object containing several attributes to describe the
    current graphics environment. If this is called before
    ``pygame.display.set_mode()`` some platforms can provide information about
    the default display mode. This can also be called after setting the display
    mode to verify specific display options were satisfied. The VidInfo object
    has several attributes:

    .. code-block:: text

      hw:         1 if the display is hardware accelerated
      wm:         1 if windowed display modes can be used
      video_mem:  The megabytes of video memory on the display.
                  This is 0 if unknown
      bitsize:    Number of bits used to store each pixel
      bytesize:   Number of bytes used to store each pixel
      masks:      Four values used to pack RGBA values into pixels
      shifts:     Four values used to pack RGBA values into pixels
      losses:     Four values used to pack RGBA values into pixels
      blit_hw:    1 if hardware Surface blitting is accelerated
      blit_hw_CC: 1 if hardware Surface colorkey blitting is accelerated
      blit_hw_A:  1 if hardware Surface pixel alpha blitting is
                  accelerated
      blit_sw:    1 if software Surface blitting is accelerated
      blit_sw_CC: 1 if software Surface colorkey blitting is
                  accelerated
      blit_sw_A:  1 if software Surface pixel alpha blitting is
                  accelerated
      current_h, current_w:  Height and width of the current video
                  mode, or of the desktop mode if called before
                  the display.set_mode is called. They are -1 on error.
      pixel_format: The pixel format of the display Surface as a string.
                  E.g PIXELFORMAT_RGB888.

    .. versionchanged:: 2.4.0 ``pixel_format`` attribute added.
    """

def get_wm_info() -> dict[str, int]:
    """Get information about the current windowing system.

    Creates a dictionary filled with string keys. The strings and values are
    arbitrarily created by the system. Some systems may have no information and
    an empty dictionary will be returned. Most platforms will return a "window"
    key with the value set to the system id for the current display.

    .. versionaddedold:: 1.7.1
    """

def get_desktop_sizes() -> list[tuple[int, int]]:
    """Get sizes of active desktops.

    This function returns the sizes of the currently configured
    virtual desktops as a list of (x, y) tuples of integers.

    The length of the list is not the same as the number of attached monitors,
    as a desktop can be mirrored across multiple monitors. The desktop sizes
    do not indicate the maximum monitor resolutions supported by the hardware,
    but the desktop size configured in the operating system.

    In order to fit windows into the desktop as it is currently configured, and
    to respect the resolution configured by the operating system in fullscreen
    mode, this function *should* be used to replace many use cases of
    ``pygame.display.list_modes()`` whenever applicable.

    .. versionaddedold:: 2.0.0
    """

def list_modes(
    depth: int = 0,
    flags: int = FULLSCREEN,
    display: int = 0,
) -> list[tuple[int, int]]:
    """Get list of available fullscreen modes.

    This function returns a list of possible sizes for a specified color
    depth. The return value will be an empty list if no display modes are
    available with the given arguments. A return value of ``-1`` means that
    any requested size should work (this is likely the case for windowed
    modes). Mode sizes are sorted from biggest to smallest.

    If depth is ``0``, the current/best color depth for the display is used.
    The flags defaults to ``pygame.FULLSCREEN``, but you may need to add
    additional flags for specific fullscreen modes.

    The display index ``0`` means the default display is used.

    Since pygame 2.0, ``pygame.display.get_desktop_sizes()`` has taken over
    some use cases from ``pygame.display.list_modes()``:

    To find a suitable size for non-fullscreen windows, it is preferable to
    use ``pygame.display.get_desktop_sizes()`` to get the size of the *current*
    desktop, and to then choose a smaller window size. This way, the window is
    guaranteed to fit, even when the monitor is configured to a lower resolution
    than the maximum supported by the hardware.

    To avoid changing the physical monitor resolution, it is also preferable to
    use ``pygame.display.get_desktop_sizes()`` to determine the fullscreen
    resolution. Developers are strongly advised to default to the current
    physical monitor resolution unless the user explicitly requests a different
    one (e.g. in an options menu or configuration file).

    .. versionchangedold:: 1.9.5 ``display`` argument added
    """

def mode_ok(
    size: IntPoint,
    flags: int = 0,
    depth: int = 0,
    display: int = 0,
) -> int:
    """Pick the best color depth for a display mode.

    This function uses the same arguments as ``pygame.display.set_mode()``. It
    is used to determine if a requested display mode is available. It will
    return ``0`` if the display mode cannot be set. Otherwise it will return a
    pixel depth that best matches the display asked for.

    Usually the depth argument is not passed, but some platforms can support
    multiple display depths. If passed it will hint to which depth is a better
    match.

    The function will return ``0`` if the passed display flags cannot be set.

    The display index ``0`` means the default display is used.

    .. versionchangedold:: 1.9.5 ``display`` argument added
    """

def gl_get_attribute(flag: int, /) -> int:
    """Get the value for an OpenGL flag for the current display.

    After calling ``pygame.display.set_mode()`` with the ``pygame.OPENGL`` flag,
    it is a good idea to check the value of any requested OpenGL attributes. See
    ``pygame.display.gl_set_attribute()`` for a list of valid flags.
    """

def gl_set_attribute(flag: int, value: int, /) -> None:
    """Request an OpenGL display attribute for the display mode.

    When calling ``pygame.display.set_mode()`` with the ``pygame.OPENGL`` flag,
    Pygame automatically handles setting the OpenGL attributes like color and
    double-buffering. OpenGL offers several other attributes you may want control
    over. Pass one of these attributes as the flag, and its appropriate value.
    This must be called before ``pygame.display.set_mode()``.

    Many settings are the requested minimum. Creating a window with an OpenGL context
    will fail if OpenGL cannot provide the requested attribute, but it may for example
    give you a stencil buffer even if you request none, or it may give you a larger
    one than requested.

    The ``OPENGL`` flags are

    ::

        GL_ALPHA_SIZE, GL_DEPTH_SIZE, GL_STENCIL_SIZE, GL_ACCUM_RED_SIZE,
        GL_ACCUM_GREEN_SIZE,  GL_ACCUM_BLUE_SIZE, GL_ACCUM_ALPHA_SIZE,
        GL_MULTISAMPLEBUFFERS, GL_MULTISAMPLESAMPLES, GL_STEREO

    :const:`GL_MULTISAMPLEBUFFERS`

        Whether to enable multisampling anti-aliasing.
        Defaults to 0 (disabled).
        Set ``GL_MULTISAMPLESAMPLES`` to a value
        above 0 to control the amount of anti-aliasing.
        A typical value is 2 or 3.

    :const:`GL_STENCIL_SIZE`

        Minimum bit size of the stencil buffer. Defaults to 0.

    :const:`GL_DEPTH_SIZE`

        Minimum bit size of the depth buffer. Defaults to 16.

    :const:`GL_STEREO`

        1 enables stereo 3D. Defaults to 0.

    :const:`GL_BUFFER_SIZE`

        Minimum bit size of the frame buffer. Defaults to 0.

    .. versionaddedold:: 2.0.0 Additional attributes:

    ::

        GL_ACCELERATED_VISUAL,
        GL_CONTEXT_MAJOR_VERSION, GL_CONTEXT_MINOR_VERSION,
        GL_CONTEXT_FLAGS, GL_CONTEXT_PROFILE_MASK,
        GL_SHARE_WITH_CURRENT_CONTEXT,
        GL_CONTEXT_RELEASE_BEHAVIOR,
        GL_FRAMEBUFFER_SRGB_CAPABLE

    :const:`GL_CONTEXT_PROFILE_MASK`

        Sets the OpenGL profile to one of these values:

        ::

            GL_CONTEXT_PROFILE_CORE             disable deprecated features
            GL_CONTEXT_PROFILE_COMPATIBILITY    allow deprecated features
            GL_CONTEXT_PROFILE_ES               allow only the ES feature
                                                subset of OpenGL

    :const:`GL_ACCELERATED_VISUAL`

        Set to 1 to require hardware acceleration, or 0 to force software render.
        By default, both are allowed.
    """

def get_active() -> bool:
    """Returns True when the display is active on the screen.

    Returns True when the display Surface is considered actively
    renderable on the screen and may be visible to the user. This is
    the default state immediately after ``pygame.display.set_mode()``.
    This method may return True even if the application is fully hidden
    behind another application window.

    This will return False if the display Surface has been iconified or
    minimized (either via ``pygame.display.iconify()`` or via an OS
    specific method such as the minimize-icon available on most
    desktops).

    The method can also return False for other reasons without the
    application being explicitly iconified or minimized by the user.  A
    notable example being if the user has multiple virtual desktops and
    the display Surface is not on the active virtual desktop.

    .. note:: This function returning True is unrelated to whether the
        application has input focus.  Please see
        ``pygame.key.get_focused()`` and ``pygame.mouse.get_focused()``
        for APIs related to input focus.
    """

def iconify() -> bool:
    """Iconify the display surface.

    Request the window for the display surface be iconified or hidden. Not all
    systems and displays support an iconified display. The function will return
    True if successful.

    When the display is iconified ``pygame.display.get_active()`` will return
    ``False``. The event queue should receive an ``ACTIVEEVENT`` event when the
    window has been iconified. Additionally, the event queue also receives a
    ``WINDOWEVENT_MINIMIZED`` event when the window has been iconified on pygame 2.
    """

def toggle_fullscreen() -> int:
    """Switch between fullscreen and windowed displays.

    Switches the display window between windowed and fullscreen modes.
    Display driver support is not great when using pygame 1, but with
    pygame 2 it is the most reliable method to switch to and from fullscreen.

    Supported display drivers in pygame 1:

        * x11 (Linux/Unix)
        * wayland (Linux/Unix)

    Supported display drivers in pygame 2:

        * windows (Windows)
        * x11 (Linux/Unix)
        * wayland (Linux/Unix)
        * cocoa (OSX/Mac)

    .. note:: :func:`toggle_fullscreen` doesn't work on Windows
        unless the window size is in :func:`pygame.display.list_modes()` or
        the window is created with the flag ``pygame.SCALED``.
        See `issue #1221 <https://github.com/pygame-community/pygame-ce/issues/1221>`_.
    """

@deprecated("since 2.1.4. Removed in SDL3")
def set_gamma(red: float, green: float = ..., blue: float = ..., /) -> bool:
    """Change the hardware gamma ramps.

    DEPRECATED: This functionality will go away in SDL3.

    Set the red, green, and blue gamma values on the display hardware. If the
    green and blue arguments are not passed, they will both be the same as red.
    Not all systems and hardware support gamma ramps, if the function succeeds
    it will return ``True``.

    A gamma value of ``1.0`` creates a linear color table. Lower values will
    darken the display and higher values will brighten.

    .. deprecated:: 2.1.4
    """

@deprecated("since 2.1.4. Removed in SDL3")
def set_gamma_ramp(
    red: SequenceLike[int], green: SequenceLike[int], blue: SequenceLike[int], /
) -> bool:
    """Change the hardware gamma ramps with a custom lookup.

    DEPRECATED: This functionality will go away in SDL3.

    Set the red, green, and blue gamma ramps with an explicit lookup table. Each
    argument should be sequence of 256 integers. The integers should range
    between ``0`` and ``0xffff``. Not all systems and hardware support gamma
    ramps, if the function succeeds it will return ``True``.

    .. deprecated:: 2.1.4
    """

def set_icon(surface: Surface, /) -> None:
    """Change the system image for the display window.

    Sets the runtime icon the system will use to represent the display window.
    All windows default to a simple pygame logo for the window icon.

    Note that calling this function implicitly initializes ``pygame.display``, if
    it was not initialized before.

    You can pass any surface, but most systems want a smaller image around
    32x32. The image can have colorkey transparency which will be passed to the
    system.

    Some systems do not allow the window icon to change after it has been shown.
    This function can be called before ``pygame.display.set_mode()`` to create
    the icon before the display mode is set.
    """

def set_caption(title: str, icontitle: Optional[str] = None, /) -> None:
    """Set the current window caption.

    If the display has a window title, this function will change the name on the
    window. In pygame 1.x, some systems supported an alternate shorter title to
    be used for minimized displays, but in pygame 2 ``icontitle`` does nothing.
    """

def get_caption() -> tuple[str, str]:
    """Get the current window caption.

    Returns the title and icontitle of the display window. In pygame 2.x
    these will always be the same value.
    """

def set_palette(palette: SequenceLike[ColorLike], /) -> None:
    """Set the display color palette for indexed displays.

    This will change the video display color palette for 8-bit displays. This
    does not change the palette for the actual display Surface, only the palette
    that is used to display the Surface. If no palette argument is passed, the
    system default palette will be restored. The palette is a sequence of
    ``RGB`` triplets.
    """

def get_num_displays() -> int:
    """Return the number of displays.

    Returns the number of available displays. This is always 1 if
    :func:`pygame.get_sdl_version()` returns a major version number below 2.

    .. versionaddedold:: 1.9.5
    """

def get_window_size() -> tuple[int, int]:
    """Return the size of the window or screen.

    Returns the size of the window initialized with :func:`pygame.display.set_mode()`.
    This may differ from the size of the display surface if ``SCALED`` is used.

    .. versionaddedold:: 2.0.0
    """

def get_window_position() -> tuple[int, int]:
    """Return the position of the window or screen.

    Returns the position of the window initialized with :func:`pygame.display.set_mode()`.
    The position will change when the user moves the window or when the
    position is set manually with :func:`pygame.display.set_window_position()`.
    Coordinates could be negative or outside the desktop size bounds. The
    position is relative to the topleft of the primary monitor and the y coordinate
    ignores the window frame.
    """

def set_window_position(position: Point) -> None:
    """Set the current window position.

    Sets the position of the window initialized with :func:`pygame.display.set_mode()`.
    This differs from updating environment variables as this function can be
    called after the display has been initialised. The position is expected to
    be relative to the topleft of the primary monitor. The y coordinate will
    ignore the window frame (y = 0 means the frame is hidden). The user will
    still be able to move the window after this call. See also
    :func:`pygame.display.get_window_position()`.
    """

def get_allow_screensaver() -> bool:
    """Return whether the screensaver is allowed to run.

    Return whether screensaver is allowed to run whilst the app is running. Default
    is ``False``. By default pygame does not allow the screensaver during game
    play.

    .. note:: Some platforms do not have a screensaver or support
        disabling the screensaver.  Please see
        :func:`pygame.display.set_allow_screensaver()` for
        caveats with screensaver support.

    .. versionaddedold:: 2.0.0
    """

def set_allow_screensaver(value: bool = True) -> None:
    """Set whether the screensaver may run.

    Change whether screensavers should be allowed whilst the app is running.
    The default value of the argument to the function is True.
    By default pygame does not allow the screensaver during game play.

    If the screensaver has been disallowed due to this function, it will automatically
    be allowed to run when :func:`pygame.quit()` is called.

    It is possible to influence the default value via the environment variable
    ``SDL_HINT_VIDEO_ALLOW_SCREENSAVER``, which can be set to either ``0`` (disable)
    or ``1`` (enable).

    .. note:: Disabling screensaver is subject to platform support.
        When platform support is absent, this function will
        silently appear to work even though the screensaver state
        is unchanged. The lack of feedback is due to SDL not
        providing any supported method for determining whether
        it supports changing the screensaver state.

    .. versionaddedold:: 2.0.0
    """

def is_fullscreen() -> bool:
    """Returns True if the pygame window created by pygame.display.set_mode() is in full-screen mode.

    Edge cases:
    If the window is in windowed mode, but maximized, this will return `False`.
    If the window is in "borderless fullscreen" mode, this will return `True`.

    .. versionadded:: 2.2.0
    """

def is_vsync() -> bool:
    """Returns True if vertical synchronisation for pygame.display.flip() and pygame.display.update() is enabled.

    .. versionadded:: 2.2.0
    """

def get_current_refresh_rate() -> int:
    """Returns the screen refresh rate or 0 if unknown.

    The screen refresh rate for the current window. In windowed mode, this
    should be equal to the refresh rate of the desktop the window is on.

    If no window is open, an exception is raised.

    When a constant refresh rate cannot be determined, 0 is returned.

    .. versionadded:: 2.2.0
    """

def get_desktop_refresh_rates() -> list[int]:
    """Returns the screen refresh rates for all displays (in windowed mode).

    If the current window is in full-screen mode, the actual refresh rate for
    that window can differ.

    This is safe to call when no window is open (i.e. before any calls to
    :func:`pygame.display.set_mode()`

    When a constant refresh rate cannot be determined, 0 is returned for that
    desktop.

    .. versionadded:: 2.2.0
    """

def message_box(
    title: str,
    message: Optional[str] = None,
    message_type: Literal["info", "warn", "error"] = "info",
    parent_window: Optional[Window] = None,
    buttons: SequenceLike[str] = ("OK",),
    return_button: int = 0,
    escape_button: Optional[int] = None,
) -> int:
    """Create a native GUI message box.

    :param str title: A title string.
    :param str message: A message string. If this parameter is set to ``None``, the message will be the title.
    :param str message_type: Set the type of message_box, could be ``"info"``, ``"warn"`` or ``"error"``.
    :param pygame.Window parent_window: The parent window of the message box.
    :param tuple buttons: An optional sequence of button name strings to show to the user.
    :param int return_button: Button index to use if the return key is hit, ``0`` by default.
    :param int escape_button: Button index to use if the escape key is hit, ``None`` for no button linked by default.

    :return: The index of the button that was pushed.

    This function should be called on the thread that ``set_mode()`` is called.
    It will block execution of that thread until the user clicks a button or
    closes the message_box.

    This function may be called at any time, even before ``pygame.init()``.

    Negative values of ``return_button`` and ``escape_button`` are allowed
    just like standard Python list indexing.

    .. versionadded:: 2.4.0
    """
