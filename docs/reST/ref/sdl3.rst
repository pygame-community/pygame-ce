SDL2 and SDL3 builds
====================

pygame-ce can be built against SDL2 or SDL3. SDL2 is the default and remains
the compatibility target for the legacy build configuration and WebAssembly
builds. Native SDL3 builds are selected explicitly with::

   python dev.py build --sdl3

The Meson option is also available directly as ``-Dsdl_api=3``. SDL3 native
builds are supported on Linux, macOS, and Windows when SDL3, SDL3_image,
SDL3_ttf, and SDL3_mixer are available. The companion libraries are optional
in the same way as their SDL2 counterparts, so modules depending on an absent
library are not installed.

The private :mod:`pygame._sdl2` namespace is an SDL2-only compatibility API.
Importing it from an SDL3 build raises :class:`ImportError`; SDL3 builds
instead install the SDL3-native :mod:`pygame._audio` and
:mod:`pygame._sdl3_mixer` modules. The legacy :mod:`pygame.mixer` and
:mod:`pygame.mixer.music` APIs are not aliases for those modules and are not
available in SDL3 builds.

Emscripten and Pyodide builds remain SDL2-only until SDL3 libraries and
bindings are available for those platforms. Briefcase packaging is likewise
limited to native desktop targets. PyInstaller packages the SDL runtime
libraries that match the SDL major used by the pygame build.