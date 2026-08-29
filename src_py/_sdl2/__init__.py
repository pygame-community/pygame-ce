from pygame.base import get_sdl_version

if get_sdl_version()[0] >= 3:
    raise ImportError(
        "pygame._sdl2 is only available when pygame is built with SDL2"
    )


if __import__("sys").platform not in ("wasi", "emscripten"):
    from .audio import *  # pylint: disable=wildcard-import; lgtm[py/polluting-import]
    from .sdl2 import *  # pylint: disable=wildcard-import; lgtm[py/polluting-import]
    from .video import *  # pylint: disable=wildcard-import; lgtm[py/polluting-import]
