import os
import platform
import warnings
import pygame

if "PYGAME_HIDE_SUPPORT_PROMPT" not in os.environ:
    print(
        f"pygame-ce {pygame.version.ver} (SDL {'.'.join(map(str, pygame.base.get_sdl_version()))}, "
        f"Python {platform.python_version()})"
    )

    pygame.print_debug_info()

warnings.filterwarnings("default")

del os, platform, warnings
