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
def get_sdl_ttf_version(linked: bool = True) -> tuple[int, int, int]: ...
def get_default_font() -> str: ...
def get_fonts() -> list[str]: ...
def match_font(
    name: str | bytes | Iterable[str | bytes],
    bold: Hashable = False,
    italic: Hashable = False,
) -> str | None: ...
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
    def size(self, text: str | bytes, /) -> tuple[int, int]: ...
    def set_underline(self, value: bool, /) -> None: ...
    def get_underline(self) -> bool: ...
    def set_strikethrough(self, value: bool, /) -> None: ...
    def get_strikethrough(self) -> bool: ...
    def set_bold(self, value: bool, /) -> None: ...
    def get_bold(self) -> bool: ...
    def set_italic(self, value: bool, /) -> None: ...
    def metrics(
        self, text: str | bytes, /
    ) -> list[tuple[int, int, int, int, int] | None]: ...
    def get_italic(self) -> bool: ...
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

    def get_point_size(self) -> int: ...
    def set_point_size(self, val: int, /) -> None: ...
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
