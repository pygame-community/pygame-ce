from pygame.version import SDL

if __import__("sys").platform not in ("wasi", "emscripten"):
    if SDL < (3, 0, 0):
        from .audio import *  # pylint: disable=wildcard-import; lgtm[py/polluting-import]
    from .sdl2 import *  # pylint: disable=wildcard-import; lgtm[py/polluting-import]

    if SDL < (3, 0, 0):
        from .video import *  # pylint: disable=wildcard-import; lgtm[py/polluting-import]
