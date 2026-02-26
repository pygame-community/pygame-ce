import fractions
from enum import IntEnum

# non-marked functions will eventually be obsolete
import pygame._base_display as _base_display
from pygame._base_display import (
    Info,
    flip,
    get_active,
    get_allow_screensaver,  #
    get_caption,
    get_current_refresh_rate,
    get_desktop_refresh_rates,
    get_desktop_sizes,
    get_driver,  #
    get_init,  #
    get_num_displays,
    get_surface,
    get_window_position,
    get_window_size,
    get_wm_info,
    gl_get_attribute,  #
    gl_set_attribute,  #
    iconify,
    init,  #
    is_fullscreen,
    is_vsync,
    list_modes,
    message_box,  #
    mode_ok,
    set_allow_screensaver,  #
    set_caption,
    set_gamma,  # already deprecated
    set_gamma_ramp,  # already deprecated
    set_icon,
    set_mode,
    set_palette,
    set_window_position,
    toggle_fullscreen,
    update,
)
from pygame.version import SDL


class DisplayOrientation(IntEnum):
    # Constants match SDL_DisplayOrientation
    UNKNOWN = 0
    LANDSCAPE = 1
    LANDSCAPE_FLIPPED = 2
    PORTRAIT = 3
    PORTRAIT_FLIPPED = 4


_displays = {}


def _get_display(ID, unplugged=False):
    if unplugged:
        display = None
        if ID in _displays:
            display = _displays[ID]
            del _displays[ID]
        return display
    if ID in _displays:
        return _displays[ID]
    if not isinstance(ID, int):
        raise TypeError("Display ID must be an integer.")
    if not _base_display.is_valid_id(ID):
        raise ValueError("Invalid Display ID.")
    display = Display.__new__(Display)
    display._id = ID
    _displays[ID] = display
    return display


class DisplayMode:
    # (display ID, width, height, pixel density, refresh rate numerator, refresh rate denominator)
    _mode_data: tuple

    def __str__(self):
        return f"<DisplayMode {self.width}x{self.height}, {float(self.refresh_rate)}hz>"

    __repr__ = __str__

    @property
    def display(self):
        return _get_display(self._mode_data[0])

    # pixel_format ?

    @property
    def width(self):
        return self._mode_data[1]

    @property
    def height(self):
        return self._mode_data[2]

    if SDL >= (3, 0, 0):

        @property
        def pixel_density(self):
            return self._mode_data[3]

    @property
    def refresh_rate(self):
        return fractions.Fraction(self._mode_data[4], self._mode_data[5])


class Display:
    _id: int

    def __init__(self):
        raise RuntimeError(
            "Explicit initialization of 'Display' is forbidden. "
            "Use 'pygame.display.get_displays', 'pygame.display.get_primary_display' or 'Display.from_...' instead."
        )

    def __eq__(self, display):
        if isinstance(display, Display):
            return self._id == display._id
        return NotImplemented

    def __hash__(self):
        return hash(self._id)

    def __str__(self):
        bounds = self.bounds
        return f"<Display {self.name} {bounds.w}x{bounds.h}>"

    __repr__ = __str__

    @property
    def name(self):
        return _base_display.get_name(self._id)

    @property
    def bounds(self):
        return _base_display.get_bounds(self._id)

    @property
    def usable_bounds(self):
        return _base_display.get_usable_bounds(self._id)

    if SDL >= (3, 0, 0):

        @property
        def content_scale(self):
            return _base_display.get_content_scale(self._id)

    @property
    def current_mode(self):
        mode = DisplayMode()
        mode._mode_data = _base_display.get_current_mode_data(self._id)
        return mode

    @property
    def desktop_mode(self):
        mode = DisplayMode()
        mode._mode_data = _base_display.get_desktop_mode_data(self._id)
        return mode

    if SDL >= (3, 0, 0):

        @property
        def fullscreen_modes(self):
            modes = []
            for data in _base_display.get_fullscreen_modes_data(self._id):
                mode = DisplayMode()
                mode._mode_data = data
                modes.append(mode)
            return modes

    @property
    def orientation(self):
        return _base_display.get_orientation(self._id)

    if SDL >= (3, 0, 0):

        @property
        def natural_orientation(self):
            return _base_display.get_natural_orientation(self._id)

        def get_closest_fullscreen_mode(
            self, width, height, refresh_rate, include_high_density_modes=True
        ):
            mode = DisplayMode()
            mode._mode_data = _base_display.get_closest_fullscreen_mode(
                self._id, width, height, refresh_rate, include_high_density_modes
            )
            if mode._mode_data is None:
                return None
            return mode

    @classmethod
    def from_window(cls, window):
        return _get_display(_base_display.get_display_from_window(window))

    @classmethod
    def from_point(cls, point):
        return _get_display(_base_display.get_display_from_point(point))

    @classmethod
    def from_rect(cls, rect):
        return _get_display(_base_display.get_display_from_rect(rect))


def get_primary_display():
    return _get_display(_base_display.get_primary_display())


def get_displays():
    return [_get_display(_id) for _id in _base_display.get_displays()]


def quit():
    # override quit behavior to clean Python-only side
    _displays.clear()
    _base_display.quit()


del IntEnum, SDL
