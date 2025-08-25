from typing import Optional, Union

from pygame.locals import WINDOWPOS_UNDEFINED
from pygame.rect import Rect
from pygame.surface import Surface
from pygame.typing import Point, RectLike
from typing_extensions import deprecated  # added in 3.13

def get_grabbed_window() -> Optional[Window]: ...

class Window:
    """Pygame object that represents a window.

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

    Event behavior if multiple windows are created: When the close button is
    pressed, a ``WINDOWCLOSE`` event is sent. You need to explicitly destroy
    the window. Note that the event ``QUIT`` will only be sent if all
    windows have been destroyed.

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
    """

    def __init__(
        self,
        title: str = "pygame window",
        size: Point = (640, 480),
        position: Union[int, Point] = WINDOWPOS_UNDEFINED,
        *,
        fullscreen: bool = ...,
        fullscreen_desktop: bool = ...,
        opengl: bool = ...,
        vulkan: bool = ...,
        hidden: bool = ...,
        borderless: bool = ...,
        resizable: bool = ...,
        minimized: bool = ...,
        maximized: bool = ...,
        mouse_grabbed: bool = ...,
        keyboard_grabbed: bool = ...,
        input_focus: bool = ...,
        mouse_focus: bool = ...,
        allow_high_dpi: bool = ...,
        mouse_capture: bool = ...,
        always_on_top: bool = ...,
        utility: bool = ...,
    ) -> None: ...

    grab_mouse: bool
    """Get or set the window's mouse grab mode.

    When this attribute is set to ``True``, the window will try to confine the mouse
    cursor to itself.

    Note this only set the "mode" of grab. The mouse may be confined to another window
    depending on the window focus. To get if the mouse is currently restricted to this
    window, please use :attr:`mouse_grabbed`.

    .. seealso:: :attr:`mouse_grabbed`

    .. versionadded:: 2.4.0
    """

    grab_keyboard: bool
    """Get or set the window's keyboard grab mode.

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
    """

    @property
    def mouse_grabbed(self) -> bool:
        """Get if the mouse cursor is confined to the window (**read-only**).

        Get if the mouse cursor is currently grabbed and confined to the window.

        Roughly equivalent to this expression:

        ::

           win.grab_mouse and (win is get_grabbed_window())

        .. seealso:: :attr:`grab_mouse`

        .. versionadded:: 2.4.0
        """

    @property
    def keyboard_grabbed(self) -> bool:
        """Get if the keyboard shortcuts are captured by the window (**read-only**).

        Get if the keyboard shortcuts are currently grabbed and captured by the window.

        Roughly equivalent to this expression:

        ::

           win.grab_keyboard and (win is get_grabbed_window())

        This attribute requires SDL 2.0.16+.

        .. seealso:: :attr:`grab_keyboard`

        .. versionadded:: 2.4.0
        """

    @property
    def focused(self) -> bool:
        """Get if the window is focused (**read-only**).

        Get if the window is currently focused. The same result can be achieved using
        the ``WINDOWFOCUSGAINED`` and ``WINDOWFOCUSLOST`` events.

        Use :meth:`focus` to focus and raise the window.

        .. versionadded:: 2.5.2
        """
    title: str
    """Get or set the window title.

    An empty string means that no title is set.
    """

    resizable: bool
    """Get or set whether the window is resizable."""

    borderless: bool
    """Gets or sets whether the window is borderless.

    .. note:: You can't change the border state of a fullscreen window.
    """

    always_on_top: bool
    """Get or set whether the window is always on top.

    Setting the always-on-top mode requires SDL 2.0.16+.

    .. versionadded:: 2.3.1
    """

    @property
    def id(self) -> int:
        """Get the unique window ID (**read-only**)."""

    @property
    def mouse_rect(self) -> Optional[Rect]:
        """Get or set the mouse confinement rectangle of the window.

        Setting this attribute to a rect-like object confines the
        cursor to the specified area of this window.

        This attribute can be None, meaning that there is no mouse rect.

        Note that this does NOT grab the cursor, it only defines the area a
        cursor is restricted to when the window has mouse focus.

        .. versionadded:: 2.4.0
        """

    @mouse_rect.setter
    def mouse_rect(self, value: Optional[RectLike]) -> None: ...
    @property
    def size(self) -> tuple[int, int]:
        """Get or set the window size in pixels."""

    @size.setter
    def size(self, value: Point) -> None: ...
    @property
    def minimum_size(self) -> tuple[int, int]:
        """Get or set the minimum size of the window's client area.

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
        """

    @minimum_size.setter
    def minimum_size(self, value: Point) -> None: ...
    @property
    def maximum_size(self) -> tuple[int, int]:
        """Get or set the maximum size of the window's client area.

        Initial value is ``(0, 0)``.

        Raises a ``ValueError`` if negative values are provided or
        if the width or height provided are less than set minimum
        width or height respectively.

        .. seealso:: :attr:`minimum_size`.

        .. versionadded:: 2.4.0
        """

    @maximum_size.setter
    def maximum_size(self, value: Point) -> None: ...
    @property
    def position(self) -> tuple[int, int]:
        """Get or set the window position in screen coordinates.

        The position may be a tuple of (x, y) coordinates or ``WINDOWPOS_CENTERED`` or
        ``WINDOWPOS_UNDEFINED``. The origin is the topleft of the main display.
        """

    @position.setter
    def position(self, value: Union[int, Point]) -> None: ...
    opacity: float
    """Get or set the window opacity, between 0.0 (fully transparent) and 1.0 (fully opaque)."""

    @property
    def opengl(self) -> bool:
        """Get if the window supports OpenGL.

        ``True`` if the ``Window`` has an OpenGL context associated with it, ``False`` otherwise

        .. versionadded:: 2.5.0
        """

    @property
    def utility(self) -> bool:
        """Get if the window is an utility window (**read-only**).

        ``True`` if the window doesn't appear in the task bar, ``False`` otherwise.
        This only works for X11 and Windows, for other platforms, creating ``Window(utility=True)`` won't change anything.

        .. versionadded:: 2.5.3
        """

    @classmethod
    @deprecated(
        "since 2.4.0. Use either the display module or the Window class with get_surface and flip. Try not to mix display and Window"
    )
    def from_display_module(cls) -> Window:
        """Create a Window object using window data from display module.

        **DON'T USE THIS!** If you want to draw to a surface and use the window
        API, use :func:`Window.get_surface` and :func:`Window.flip`.

        Create a Window object that uses the same window data from the :mod:`pygame.display` module, created upon calling
        :func:`pygame.display.set_mode`.

        .. deprecated:: 2.4.0
        """

    def get_surface(self) -> Surface:
        """Get the window surface.

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
        """

    def flip(self) -> None:
        """Update the display surface to the window.

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
        """

    def set_windowed(self) -> None:
        """Enable windowed mode (exit fullscreen).

        .. seealso:: :func:`set_fullscreen`
        """

    def set_fullscreen(self, desktop: bool = False) -> None:
        """Enter fullscreen.

        :param bool desktop: If ``True``, use the current desktop resolution.
            If ``False``, change the fullscreen resolution to the window size.

        .. seealso:: :meth:`set_windowed`.
        """

    def destroy(self) -> None:
        """Destroy the window.

        Destroys the internal window data of this Window object. This method is
        called automatically when this Window object is garbage collected, so
        there usually aren't any reasons to call it manually.

        Other methods that try to manipulate that window data will raise an error.
        """

    def hide(self) -> None:
        """Hide the window."""

    def show(self) -> None:
        """Show the window."""

    def focus(self, input_only: bool = False) -> None:
        """Set the window to be focused.

        Raises the window above other windows and sets the input focus.

        :param input_only: if ``True``, the window will be given input focus
                                but may be completely obscured by other windows.
                                Only supported on X11. This has been deprecated and
                                may be removed in a future version.

        .. deprecated:: 2.5.3 ``input_only`` argument
        """

    def restore(self) -> None:
        """Restore the size and position of a minimized or maximized window."""

    def maximize(self) -> None:
        """Maximize the window."""

    def minimize(self) -> None:
        """Minimize the window."""

    def set_icon(self, icon: Surface, /) -> None:
        """Set the window icon.

        :param Surface surface: A Surface to use as the icon.
        """

    def set_modal_for(self, parent: Window, /) -> None:
        """Set the window as a modal for a parent window.

        :param Window parent: The parent window.

        .. note:: This function is only supported on X11.
        """

    def flash(self, operation: int, /) -> None:
        """Flash a window to demand attention from the user.

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
        """
    relative_mouse: bool
