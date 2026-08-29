"""Policy helpers for the retired SDL2-only build configuration."""


def reject_sdl3(argv):
    if "-sdl3" in argv:
        raise SystemExit(
            "The legacy buildconfig path supports SDL2 only. "
            'Use "python dev.py build --sdl3" for an SDL3 build.'
        )