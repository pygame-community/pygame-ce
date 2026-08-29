SDL2 and SDL3 builds
====================

pygame-ce can be built against SDL2 or SDL3. SDL2 is the default and remains
the compatibility target for the legacy build configuration. Native SDL3
builds are selected explicitly with::

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


SDL3 WebAssembly
----------------
SDL3 Emscripten builds are supported experimentally for both pygbag and
Pyodide. They consume a dependency prefix containing SDL3 and its companion
libraries instead of using Emscripten's SDL2 ports. The prefix must have this
layout::

   $PG_WASM_SDL_ROOT/
       include/SDL3/
       lib/libSDL3.a
       lib/libSDL3_image.a
       lib/libSDL3_ttf.a
       lib/libSDL3_mixer.a

For ``dev.py`` builds, set ``PYGAME_EMSCRIPTEN_SDL_ROOT`` to that prefix. The
generated cross file passes it as ``emscripten_sdl_root``; a missing prefix is
an error and does not silently select SDL2. The ordinary SDL3 renderer is the
WebGL path, with WebGL 1 and 2 enabled by the Emscripten link settings.

The repository includes a reproducible prefix builder. It checks out the
release tags and their exact submodule commits, then builds static libraries
with Emscripten::

   python buildconfig/build_emscripten_sdl3.py \
       --prefix /tmp/pygame-sdl3 \
       --emsdk-root /path/to/emsdk

The default web bundle enables PNG, JPEG, and WebP image loading, standard
SDL_ttf font shaping, and SDL_mixer's self-contained WAV, Ogg Vorbis, FLAC,
MP3, and MIDI decoders. Optional native codecs can be added by maintaining a
larger prefix outside this builder.

Optional WebGPU surface support can be enabled for SDL3 with::

   meson setup build -Dsdl_api=3 -Dwebgpu=enabled \
       -Dsdl3webgpu_root=/path/to/sdl3webgpu -Dwebgpu_root=/path/to/webgpu

The bridge follows the ``SDL_GetWGPUSurface`` API from
`sdl3webgpu <https://github.com/eliemichel/sdl3webgpu>`_. Its Emscripten
implementation uses the browser canvas selector and is not required for the
WebGL renderer. The copied reference files retain their MIT license notice.

SDL2 WebAssembly builds continue to use the existing Emscripten ports. The
legacy ``buildconfig`` path remains SDL2-only. Briefcase packaging is likewise
limited to native desktop targets, and PyInstaller packages the SDL runtime
libraries that match the SDL major used by the pygame build.


**Recommendation**

Implement SDL3 for the standalone Emscripten/pygbag toolchain first, then use
Pyodide with the same binding and dependency layers. SDL3 core and the
companion libraries are built into one pinned prefix; the existing SDL2
`embuilder` ports remain unchanged.

Keep the current SDL2 WebAssembly builds unchanged until SDL3 passes its own build and runtime gates.

```mermaid
flowchart TD
    A[SDL-aware pygame Cython implementation] --> B[pygame-owned pgsdl adapter API]
    B --> C[SDL2 adapter]
    B --> D[SDL3 adapter]
    C --> E[Native SDL2 and existing WASM]
    D --> F[Native SDL3]
    D --> G[Emscripten SDL3]
    D --> H[Pyodide SDL3]
    I[Reusable web dependency bundle] --> G
    I --> H
```

**1. Establish the WebAssembly support contract**

Use a short feasibility branch before changing the default build behavior.

Define:

- Supported Emscripten version and Python version.
- SDL3, SDL3_image, SDL3_ttf, and SDL3_mixer versions or commits.
- Whether the first release supports only the software/2D renderer and WebGL.
- Whether audio, microphone capture, filesystem persistence, OpenGL, and joystick support are included.
- Whether SDL3 builds remain single-extension/static builds, as they are today.

The SDL documentation confirms that SDL3 itself can be built with Emscripten and linked as `libSDL3.a`. The uncertain part is the availability and behavior of the companion libraries. Build a minimal SDL3 application plus one minimal application for each companion library before porting pygame.

The SDL3 WebAssembly path remains experimental until a pinned dependency bundle
has passed browser import, display, event, and rendering smoke and acceptance tests.

**2. Create a reusable SDL binding layer**

The current Cython declarations are tightly coupled to SDL2. For example, audio.pxd declares the SDL2 `SDL_AudioSpec` layout directly, while video.pxd declares SDL2 renderer and texture signatures.

Introduce a pygame-owned adapter interface:

- Add a stable header such as `src_c/pgsdl.h`.
- Provide SDL2 and SDL3 implementations selected by `PG_SDL3`.
- Expose pygame-owned types and functions for:
  - initialization and errors,
  - audio devices and callbacks,
  - windows and renderers,
  - textures and pixel formats,
  - surfaces and rectangles,
  - display and input queries,
  - SDL_mixer operations where the APIs are compatible.
- Use opaque handles where possible.
- Use pygame-owned audio and renderer structs instead of exposing SDL struct layouts to Cython.
- Put changed SDL2/SDL3 signatures behind C functions, not preprocessor aliases in every `.pxd`.

Then move the reusable Cython implementation into a neutral location, for example:

```text
src_c/cython/pygame/_sdl/
    audio.pyx
    video.pyx
    mixer.pyx
    sdl.pyx
    pgsdl.pxd
```

Use thin package-specific wrappers or module entry points so the same implementation can be compiled for both SDL majors.

The namespace policy should remain explicit:

- SDL2 continues to provide `pygame._sdl2`.
- SDL3 must not masquerade as `pygame._sdl2`.
- SDL3-native functionality continues to use `_audio` and `_sdl3_mixer`; add an `_sdl3` namespace only if a public/private replacement for the existing video or general SDL bindings is actually required.

This preserves the existing behavior in __init__.py while avoiding a second copy of the implementation.

**3. Fix the static WebAssembly build model**

The current Emscripten target in meson.build bundles SDL2 Cython sources into one extension. It also relies on the large `BUILD_STATIC` amalgamation in base.c.

Before enabling SDL3, audit the static include list in base.c. It currently includes SDL2-specific or SDL2-only modules such as:

- `mixer.c`
- `music.c`
- `_sdl2/controller.c`
- `_sdl2/touch.c`

The SDL3 static target should:

- Include only modules that compile against SDL3.
- Exclude the legacy SDL2 mixer and music implementations.
- Include `_base_audio.c` and `_sdl3_mixer_c.c` when their dependencies are available.
- Register the reusable Cython modules with the correct package names.
- Preserve the existing single-extension behavior required by pygbag and the Python WASM SDK.
- Avoid compiling SDL2-only declarations merely because the target is static.

Add a dedicated Meson helper or source list for the WebAssembly SDL backend instead of continuing to grow the SDL2-specific `cython_files` list.

**4. Replace hard-coded SDL2 Web dependencies**

The current SDL branches are hard-coded in meson.build:

- pygbag uses `-lSDL2`, `-lSDL2_image`, and `-lSDL2_ttf`.
- Pyodide uses `-sUSE_SDL=2` and SDL2-specific Emscripten ports.
- dev.py adds SDL2 include directories to the pygbag cross file.
- config_emsdk.py is intentionally SDL2-only.

Keep config_emsdk.py SDL2-only because the legacy build path is already retired for SDL3. Put SDL3 WebAssembly dependency handling in Meson and the WebAssembly packaging workflows.

Create one reusable dependency contract with a layout such as:

```text
$PG_WASM_SDL_ROOT/
    include/SDL3/
    lib/libSDL3.a
    lib/libSDL3_image.a
    lib/libSDL3_ttf.a
    lib/libSDL3_mixer.a
    lib/*.a
```

The provider can differ by toolchain:

- pygbag: the SDL3 CI job builds the pinned prefix next to the
    `python-wasm-sdk` archive.
- Pyodide: a `before-build` step builds the same library set into a temporary
    prefix.
- Meson consumes the prefix through one environment variable or cross-file option.

This avoids duplicating library names and include paths in meson.build, dev.py, and CI.

**5. Add SDL3 support to the pygbag toolchain**

Update dev.py so the generated Emscripten cross file:

- Selects the SDL3 include directory when `-Dsdl_api=3` is used.
- Adds the SDL3 dependency prefix to the compiler and linker paths.
- Carries the selected SDL API into the Meson configuration.
- Does not silently fall back to SDL2.

The SDL3 CI job currently builds the prefix from the pinned source tags. A
future `python-wasm-sdk` or pygame-specific distribution may ship the same
layout as a cache, but the artifact should include SDL3 companion libraries
only when they are actually supported and tested.

Keep the existing `-sUSE_SDL=2` path for SDL2. SDL3 should use the statically built SDL3 archives directly rather than relying on an SDL2-specific Emscripten setting.

Add a separate CI job or matrix entry in build-emsdk.yml with:

- the pinned SDK,
- `-Dsdl_api=3`,
- the SDL3 dependency bundle,
- a minimal browser smoke test,
- an import and surface/display test before attempting the full pygame suite.

**6. Add SDL3 support to Pyodide**

Pyodide needs a separate dependency strategy. The current configuration in pyproject.toml runs:

```text
embuilder ... sdl2 ... sdl2_ttf ... sdl2_mixer ... sdl2_image ...
```

For SDL3, replace that with one of these approaches:

1. Preferably, consume official Pyodide SDL3 packages or ports once available.
2. Otherwise, build SDL3 and its companion libraries from pinned source revisions during the Pyodide build.
3. If build time is excessive, publish a versioned SDL3 Pyodide dependency bundle and cache it in CI.

The Pyodide job should explicitly pass the Meson option for SDL3 rather than changing the global default. Keep the existing SDL2 Pyodide job until SDL3 has equivalent coverage.

The dependency build must account for:

- SDL3 CMake configuration under the Pyodide Emscripten toolchain.
- static archive ordering and transitive codec libraries,
- `-fwasm-exceptions`, relocatable code, and longjmp behavior,
- SDL3_image format selection,
- SDL3_mixer codec selection,
- freetype and harfbuzz linkage,
- exported JavaScript libraries such as `html5` where still required.

**7. Port browser-specific SDL3 behavior**

The common adapter should preserve pygame semantics, but WebAssembly needs focused handling for:

- browser user-gesture requirements before audio output,
- the single/default audio device model,
- microphone permission and capture behavior,
- WebGL-backed SDL rendering,
- canvas sizing and high-DPI display sizes,
- asynchronous filesystem or preload behavior,
- event-loop integration with pygbag and Pyodide,
- lack of conventional process termination,
- browser main-thread restrictions.

Keep WebGPU optional. SDL3’s 2D renderer running through WebGL is the default
and more widely compatible target; the SDL3 WebGPU bridge is an opt-in surface
integration for applications that already provide a WebGPU instance.

**8. Add tests in layers**

Add tests at four levels:

- **Binding compile tests:** compile the adapter and reusable Cython sources with SDL2, native SDL3, pygbag SDL3, and Pyodide SDL3.
- **Import tests:** verify SDL version reporting, `_sdl2` rejection under SDL3, and availability of `_audio` and `_sdl3_mixer`.
- **Headless runtime tests:** initialize, create a surface, load an image, render a texture, enumerate audio devices, and shut down cleanly.
- **Browser smoke tests:** run a small packaged pygame application and verify display initialization, event delivery, one rendered frame, filesystem access, and audio initialization after user interaction.

Use the existing focused test style in test before enabling the full suite. The full suite should remain separately reported because browser audio, timing, OpenGL, and filesystem tests will need exclusions or browser-specific assertions.

**9. CI and release gates**

A practical sequence is:

1. SDL3 core Emscripten proof of concept.
2. Reusable adapter compiles against native SDL2 and SDL3.
3. SDL3 pygbag build and browser smoke test.
4. SDL3 companion-library builds.
5. SDL3 Pyodide wheel build and import test.
6. Focused pygame tests on both WebAssembly targets.
7. Expanded test matrix and documentation update.
8. Only then remove the SDL3 rejection from meson.build.

The final CI matrix should retain:

- native SDL2,
- native SDL3,
- SDL2 pygbag,
- SDL3 pygbag,
- SDL2 Pyodide,
- SDL3 Pyodide.

The most important design decision is to make Cython depend on a pygame-owned ABI-neutral adapter instead of SDL headers. That lets the same binding implementation be reused by native SDL3, pygbag SDL3, and Pyodide SDL3 without creating parallel `_sdl2` and `_sdl3` copies that will drift.