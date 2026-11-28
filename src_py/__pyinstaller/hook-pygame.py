"""
This controls how PyInstaller interacts with pygame-ce when
freezing a project.

See https://pyinstaller.org/en/stable/hooks.html

This hook adds necessary icon/font files to the bundle, and makes
sure all our needed DLLs are included on Windows.
"""

import os
import platform

from pygame import __file__ as pygame_main_file

# Get pygame's folder
pygame_folder = os.path.dirname(os.path.abspath(pygame_main_file))

# datas is the variable that pyinstaller looks for while processing hooks
datas = []


# A helper to append the relative path of a resource to hook variable - datas
def _append_to_datas(file_path):
    res_path = os.path.join(pygame_folder, file_path)
    if os.path.exists(res_path):
        datas.append((res_path, "pygame"))


# First append the font file, then based on the OS, append pygame icon file
_append_to_datas("freesansbold.ttf")
if platform.system() == "Darwin":
    _append_to_datas("pygame_icon_mac.bmp")
else:
    _append_to_datas("pygame_icon.bmp")

if platform.system() == "Windows":
    from PyInstaller.utils.hooks import collect_dynamic_libs

    # In our Windows builds, some C libraries are loaded at runtime
    # as optional extras to SDL_image or SDL_mixer, rather than
    # declaring the load statically. Therefore, we need to collect
    # all binaries, not just the ones that PyInstaller thinks are used.
    binaries = collect_dynamic_libs("pygame")
