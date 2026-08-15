from collections.abc import Callable, Hashable, Iterable
from typing import Literal

from pygame.surface import Surface
from pygame.typing import ColorLike, FileLike
from typing_extensions import deprecated  # added in 3.13

# TODO: Figure out a way to type this attribute such that mypy knows it's not
# always defined at runtime
UCS4: Literal[1]

def init() -> None: ...
def quit() -> None: ...
def get_init() -> bool: ...
def get_sdl_ttf_version(linked: bool = True) -> tuple[int, int, int]:
    """
    Gets SDL_ttf version.

    Returns a tuple of integers that identify SDL_ttf's version,
    ``(major, minor, patch)``. SDL_ttf is the underlying font rendering library,
    written in C, on which pygame's font module depends. If 'linked' is True
    (the default), the function returns the version of the linked TTF library.
    Otherwise this function returns the version of TTF pygame was compiled with.

    .. versionadded:: 2.1.3
    """

def get_default_font() -> str:
    """
    Get the filename of the default font.

    Return the filename of the system font. This is not the full path to the
    file. This file can usually be found in the same directory as the font
    module, but it can also be bundled in separate archives.
    """

def get_fonts() -> list[str]:
    """Get all available fonts.

    Returns a list of all the fonts available on the system. The names of the
    fonts will be set to lowercase with all spaces and punctuation removed. This
    works on most systems, but some will return an empty list if they cannot
    find fonts.

    .. versionchanged:: 2.1.3 Checks through user fonts instead of just global fonts for Windows.
    """

def match_font(
    name: str | bytes | Iterable[str | bytes],
    bold: Hashable = False,
    italic: Hashable = False,
) -> str | None:
    """Find a specific font on the system.

    Returns the full path to a font file on the system. If bold or italic are
    set to true, this will attempt to find the correct family of font.

    The font name can also be an iterable of font names, a string of
    comma-separated font names, or a bytes of comma-separated font names, in
    which case the set of names will be searched in order.
    If none of the given names are found, None is returned.

    .. versionaddedold:: 2.0.1 Accept an iterable of font names.

    .. versionchanged:: 2.1.3 Checks through user fonts instead of just global fonts for Windows.

    Example::

        >>> pygame.font.match_font('Arial')
        'C:\\WINDOWS\\Fonts\\arial.ttf'
    """

def SysFont(
    name: str | bytes | Iterable[str | bytes] | None,
    size: int,
    bold: Hashable = False,
    italic: Hashable = False,
    constructor: Callable[[str | None, int, bool, bool], Font] | None = None,
) -> Font: ...

class Font:
    @property
    def name(self) -> str: ...
    @property
    def style_name(self) -> str: ...
    @property
    def bold(self) -> bool: ...
    @bold.setter
    def bold(self, value: bool) -> None: ...
    @property
    def italic(self) -> bool: ...
    @italic.setter
    def italic(self, value: bool) -> None: ...
    @property
    def underline(self) -> bool: ...
    @underline.setter
    def underline(self, value: bool) -> None: ...
    @property
    def strikethrough(self) -> bool: ...
    @strikethrough.setter
    def strikethrough(self, value: bool) -> None: ...
    @property
    def align(self) -> int: ...
    @align.setter
    def align(self, value: int) -> None: ...
    @property
    def point_size(self) -> int: ...
    @point_size.setter
    def point_size(self, value: int) -> None: ...
    @property
    def outline(self) -> int: ...
    @outline.setter
    def outline(self, value: int) -> None: ...
    def __init__(self, filename: FileLike | None = None, size: int = 20) -> None: ...
    def render(
        self,
        text: str | bytes | None,
        antialias: bool,
        color: ColorLike,
        bgcolor: ColorLike | None = None,
        wraplength: int = 0,
    ) -> Surface: ...
    def size(self, text: str | bytes, /) -> tuple[int, int]:
        """
        Determine the amount of space needed to render text.

        Returns the dimensions (width, height) needed to render the text.
        This can be used to help determine the positioning needed for text
        before it is rendered. It can also be used for word wrapping and other
        layout effects.

        Be aware that most fonts use kerning which adjusts the widths for
        specific letter pairs. For example, the width for "ae" will not always
        match the width for "a" + "e".
        """

    def set_underline(self, value: bool, /) -> None:
        """
        Control if text is rendered with an underline.

        When enabled, all rendered fonts will include an underline. The underline
        is always one pixel thick, regardless of font size. This can be mixed
        with the bold, italic and strikethrough modes.

        .. note:: This is the same as the :attr:`underline` attribute.
        """

    def get_underline(self) -> bool:
        """
        Check if text will be rendered with an underline.

        Return True when the font underline is enabled.

        .. note:: This is the same as the :attr:`underline` attribute.
        """

    def set_strikethrough(self, value: bool, /) -> None:
        """
        Control if text is rendered with a strikethrough.

        When enabled, all rendered fonts will include a strikethrough. The
        strikethrough is always one pixel thick, regardless of font size.
        This can be mixed with the bold, italic and underline modes.

        .. note:: This is the same as the :attr:`strikethrough` attribute.

        .. versionadded:: 2.1.3
        """

    def get_strikethrough(self) -> bool:
        """
        Check if text will be rendered with a strikethrough.

        Return True when the font strikethrough is enabled.

        .. note:: This is the same as the :attr:`strikethrough` attribute.

        .. versionadded:: 2.1.3
        """

    def set_bold(self, value: bool, /) -> None:
        """
        Enable fake rendering of bold text.

        Enables the bold rendering of text. This is a fake stretching of the font
        that doesn't look good on many font types. If possible load the font from
        a real bold font file. While bold, the font will have a different width
        than when normal. This can be mixed with the italic, underline and
        strikethrough modes.

        .. note:: This is the same as the :attr:`bold` attribute.
        """

    def get_bold(self) -> bool:
        """
        Check if text will be rendered bold.

        Return True when the font bold rendering mode is enabled.

        .. note:: This is the same as the :attr:`bold` attribute.
        """

    def set_italic(self, value: bool, /) -> None:
        """
        Enable fake rendering of italic text.

        Enables fake rendering of italic text. This is a fake skewing of the font
        that doesn't look good on many font types. If possible load the font from
        a real italic font file. While italic the font will have a different
        width than when normal. This can be mixed with the bold, underline and
        strikethrough modes.

        .. note:: This is the same as the :attr:`italic` attribute.
        """
    def metrics(
        self, text: str | bytes, /
    ) -> list[tuple[int, int, int, int, int] | None]:
        """
        Gets the metrics for each character in the passed string.

        The list contains tuples for each character, which contain the minimum
        ``X`` offset, the maximum ``X`` offset, the minimum ``Y`` offset, the
        maximum ``Y`` offset and the advance offset (bearing plus width) of the
        character. [(minx, maxx, miny, maxy, advance), (minx, maxx, miny, maxy,
        advance), ...]. None is entered in the list for each unrecognized
        character.

        .. versionchanged:: 2.5.4 This function now supports all unicode codepoints.
            Previously, only a subset that was representable in UCS-2 was supported.
        """

    def get_italic(self) -> bool:
        """
        Check if the text will be rendered italic.

        Return True when the font italic rendering mode is enabled.

        .. note:: This is the same as the :attr:`italic` attribute.
        """

    def get_linesize(self) -> int:
        """
        Get the line space of the font text.

        Return the height in pixels for a line of text with the font. When
        rendering multiple lines of text this is the recommended amount of space
        between lines.

        See also :meth:`set_linesize`.
        """

    def set_linesize(self, linesize: int, /) -> None:
        """
        Set the line space of the font text.

        Set the height in pixels for a line of text with the font. When rendering
        multiple lines of text this refers to the amount of space between lines.
        The value must be non-negative.

        See also :meth:`get_linesize`.

        .. versionadded:: 2.5.4
        """

    def get_height(self) -> int:
        """
        Get the height of the font.

        Return the height in pixels of the actual rendered text. This is the
        average size for each glyph in the font.
        """

    def get_point_size(self) -> int:
        """
        Get the point size of the font.

        Returns the point size of the font. Will not be accurate upon
        initializing the font object when the font name is initialized
        as ``None``.

        .. note:: This is the same as the :attr:`point_size` attribute.

        .. versionadded:: 2.3.1
        """

    def set_point_size(self, val: int, /) -> None:
        """
        Set the point size of the font.

        .. note:: This is the same as the :attr:`point_size` attribute.

        .. versionadded:: 2.3.1
        """

    def get_ascent(self) -> int:
        """
        Get the ascent of the font.

        Return the height in pixels for the font ascent. The ascent is the number
        of pixels from the font baseline to the top of the font.
        """

    def get_descent(self) -> int:
        """
        Get the descent of the font.

        Return the height in pixels for the font descent. The descent is the
        number of pixels from the font baseline to the bottom of the font.
        """

    def set_script(self, script_code: str, /) -> None:
        """
        Set the script code for text shaping.

        Sets the script used by HarfBuzz text shaping, taking a 4 character
        script code as input. For example, Hindi is written in the Devanagari
        script, for which the script code is `"Deva"`. See the full list of
        script codes in `ISO 15924 <https://www.unicode.org/iso15924/iso15924-codes.html>`_.

        This method requires pygame built with SDL_ttf 2.20.0 or above. Otherwise the
        method will raise a pygame.error.

        .. versionadded:: 2.1.4
        """

    def set_direction(self, direction: int) -> None:
        """
        Set the script direction for text shaping.

        Sets the font direction for HarfBuzz text rendering, taking in an integer
        between 0 and 3 (inclusive) as input. There are convenient constants defined
        for use in this method.

        * ``pygame.DIRECTION_LTR`` is for left-to-right text
        * ``pygame.DIRECTION_RTL`` is for right-to-left text
        * ``pygame.DIRECTION_TTB`` is for top-to-bottom text
        * ``pygame.DIRECTION_BTT`` is for bottom-to-top text

        This method requires pygame built with SDL_ttf 2.20.0 or above. Otherwise the
        method will raise a pygame.error.

        .. note:: multiline renders with :meth:`render` do not play nicely with top-to-bottom
            or bottom-to-top rendering.

        .. versionadded:: 2.1.4
        """

@deprecated("Use `Font` instead (FontType is an old alias)")
class FontType(Font): ...
