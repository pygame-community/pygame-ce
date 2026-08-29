# SDL3 Porting Plan

## Purpose

Port `pygame-ce` from SDL2 to SDL3 while preserving the pygame Python API and keeping SDL2 builds available during the migration. SDL3 should become a supported, tested build target first; making it the default is a separate release decision.

This plan covers the pygame-ce tree in `src/pygame-ce`, including the core C modules, Cython extensions, SDL_image, SDL_mixer, SDL_ttf, build configuration, CI, packaged dependencies, tests, and documentation.

## Current Baseline

The repository already has a partial port:

- `meson_options.txt` exposes `-Dsdl_api=2|3`, with SDL2 as the default.
- `meson.build` derives the SDL dependency names from `sdl_api` and defines `PG_SDL3` for SDL3 builds.
- `src_c/_pygame.h` and several core modules contain SDL3 compatibility branches.
- `dev.py build --sdl3` passes the Meson option and is the intended local entry point.
- Windows dependency downloads already contain SDL3, SDL3_image, SDL3_ttf, and SDL3_mixer archives.
- `.github/workflows/build-sdl3.yml` builds SDL3 on Linux and macOS, but currently tests only whether `pygame` imports.

Important gaps are still present:

- The legacy `buildconfig` path writes `Setup.SDL2` and searches for SDL2 headers, libraries, and DLLs.
- Windows and MSYS2 dependency discovery has SDL2-only setup functions.
- Emscripten and Pyodide link against SDL2 unconditionally.
- `_sdl2` and other C extension targets remain explicitly disabled for SDL3; `_render` and `gfxdraw` are now enabled and tested under both SDL APIs.
- Several source files contain SDL3 TODOs, removed-API workarounds, or SDL2 compatibility assumptions.
- The README dependency table and build documentation describe SDL2 only.
- The SDL3 workflow has no Windows SDL3 installation step and its full test job is disabled.

### Verified Progress

- SDL3 has been built locally with SDL 3.4.15, SDL3_image 3.5.0, SDL3_ttf 3.3.0, and SDL3_mixer 3.3.0 with old-name compatibility disabled.
- Core compatibility work is committed in `e213404bb` (`Port core compatibility paths to SDL3`).
- `gfxdraw` SDL3 support is committed in `7699d2854` (`Port gfxdraw primitives to SDL3`); its focused and neighboring draw tests pass under SDL2 and SDL3.
- `_render` SDL3 support is committed in `6a8ff81f5` (`Port _render extension to SDL3`); its focused tests pass under SDL3, and the SDL2 renderer, draw, and gfxdraw suites remain green.
- Native Meson SDL selection now reports the selected API, uses matching SDL2/SDL3 Windows runtime names, and rejects unsupported SDL3 Emscripten/Pyodide builds instead of linking SDL2 silently.
- The legacy `buildconfig` path now rejects an explicit SDL3 request; common SDL feature branches use `PG_SDL3`, and SDL surface-lock return values are normalized for core and SDL_gfx callers.
- The private `_sdl2` namespace is explicitly retained as an SDL2-only compatibility API; SDL3 builds fail at import time with a clear error and use the SDL3-native `_audio` and `_sdl3_mixer` modules instead.
- SDL3 display creation and renderer-backed resizing now translate public display indexes to opaque SDL3 display IDs and honor SDL3 boolean success returns; the focused display and font tests pass under both SDL majors.
- SDL3 audio format conversion is covered by `test/audio_test.py`; all supported `AudioFormat` values round-trip through `AudioStream`, while the `UNKNOWN` sentinel is rejected by SDL as expected. The test skips cleanly on SDL2, where `_audio` is intentionally unavailable.
- SDL3 mouse warping now passes float coordinates without the old `Uint16` wraparound; negative-coordinate behavior is covered by `test/mouse_test.py` and passes under both SDL2 and SDL3 headless drivers.

## Migration Principles

1. Keep SDL2 green until SDL3 reaches feature and release parity.
2. Make the selected SDL API a build-time property, not a runtime guess.
3. Prefer small compatibility wrappers in the pygame-owned headers over scattered version checks.
4. Compile with SDL3's old-name compatibility disabled before declaring the port complete. `SDL_ENABLE_OLD_NAMES=1` may be used temporarily, but it must not hide unresolved API changes.
5. Treat SDL_image, SDL_ttf, and SDL_mixer as separate ports with their own version and behavior checks.
6. Preserve public pygame names where practical. SDL-specific private modules need an explicit compatibility policy before their implementation is changed.
7. Every SDL3 change must retain an SDL2 build/test check unless the related code is intentionally SDL3-only.

## Phase 0: Inventory and Compatibility Contract

- [ ] Create an API inventory from SDL2 headers and the pygame source, grouped by subsystem: initialization, errors, events, display/window, input, surfaces/pixel formats, audio, timing, filesystem/RWops, OpenGL, SDL_image, SDL_ttf, SDL_mixer, joystick/controller, touch, and platform-specific code.
- [ ] Classify each SDL2 call as unchanged, renamed, signature-changed, removed, behavior-changed, or requiring emulation.
- [ ] Record the minimum supported versions for SDL3, SDL3_image, SDL3_ttf, and SDL3_mixer, and pin one tested dependency set for CI and wheels.
- [ ] Define the support matrix: native Linux, Windows, macOS, Emscripten/Pyodide, Python versions, optional modules, headless mode, audio backends, and OpenGL.
- [x] Decide whether `pygame._sdl2` remains the stable Python compatibility name when backed by SDL3, whether a new `_sdl3` namespace is needed, and which SDL2-only behavior is intentionally unavailable. `_sdl2` remains SDL2-only; SDL3 uses the native `_audio` and `_sdl3_mixer` modules.
- [ ] Add a tracking checklist or issue links for every inventory item. No subsystem should be considered complete because it merely compiles.

**Gate:** The team can state the supported SDL3/dependency versions, platform matrix, public compatibility policy, and an owner/status for every SDL-facing subsystem.

## Phase 1: Build and Dependency Infrastructure

- [x] Make Meson the single source of truth for SDL selection. Ensure `sdl_api` controls the core SDL library and all companion libraries consistently.
- [x] Add explicit SDL2 and SDL3 dependency branches where package names, include directories, link names, or transitive libraries differ. Do not rely on SDL3 old-name aliases to resolve build configuration issues.
- [x] Retire SDL3 selection from the legacy `buildconfig` path. `config.py`, `config_unix.py`, `config_darwin.py`, `config_win.py`, `config_msys2.py`, and `config_emsdk.py` reject SDL3 before SDL2 dependency discovery; the legacy path remains SDL2-only.
- [ ] Update native Linux, macOS, Windows, and manylinux dependency builds with reproducible SDL3 source/archive versions and checksums. Keep SDL2 artifacts available for the existing build path.
- [ ] Complete Windows SDL3 packaging: dependency discovery, import libraries, DLL collection, architecture-specific paths, wheel contents, and runtime loading.
- [x] Document Emscripten/Pyodide as unsupported for SDL3 until SDL3 libraries and bindings are available. The SDL2-only WASM path rejects SDL3 selection rather than silently selecting SDL2.
  - [ ] Clone and review and possibly integrate
    https://github.com/eliemichel/sdl3webgpu
    - [ ] Then add WebGL support to fallback to when WebGPU is not available?
- [ ] Update `pyproject.toml`, cibuildwheel settings, development commands, and build documentation so the selected SDL API is visible in build logs and artifacts.
- [ ] Pin the SDL3 CI builds to known releases or commits instead of cloning moving default branches.

**Gate:** A clean build succeeds for SDL2 and SDL3 on every supported native platform, and the resulting wheel contains the matching SDL runtime libraries without SDL2/SDL3 mixing.

## Phase 2: Common Headers and Compatibility Layer

- [ ] Centralize SDL2/SDL3 type aliases, return-value adapters, removed constants, and renamed functions in the existing pygame compatibility headers (`_pygame.h`, `pgcompat.*`, `pgcompat_rect.*`, and related module headers).
- [x] Replace broad `SDL_VERSION_ATLEAST` checks with the build feature flag where the build intentionally selects one SDL API. Keep version checks only when supporting multiple versions within the same SDL major release is required.
- [x] Remove the temporary `SDL_ENABLE_OLD_NAMES=1` dependency incrementally and compile with old names disabled to expose real porting gaps.
- [ ] Verify error propagation and ownership rules for SDL3 functions that changed from integer returns to boolean/void returns, especially mutexes, surfaces, windows, audio, and IO streams.
- [ ] Audit integer widths, enum types, pixel formats, audio formats, floating-point coordinates, and `SDL_Rect` edge semantics at every Python conversion boundary.
- [ ] Keep compatibility behavior in pygame terms. Do not expose SDL3 implementation details through an existing pygame API unless that behavior is intentionally documented.

**Gate:** Core headers compile cleanly with SDL2 and SDL3, with warnings enabled and no old-name compatibility macro required for the SDL3 build.

## Phase 3: Port Core Runtime Modules

Port in dependency order, testing each subsystem against both SDL APIs:

1. **Startup and event loop:** `base.c`, `event.c`, `system.c`, signal handling, initialization flags, error strings, event constants, and event queue behavior.
2. **Display and input:** `display.c`, `window.c`, `key.c`, `mouse.c`, `joystick.c`, controller support, touch input, cursors, clipboard, and scrap. Account for removed SDL3 APIs and float mouse coordinates.
3. **Surfaces and geometry:** `surface.c`, `pixelcopy.c`, `surflock.c`, `draw.c`, `scale2x.c`, `pgcompat_rect.*`, pixel formats, palettes, color keys, alpha, RLE, locks, clipping, and conversion behavior.
4. **Image and font paths:** `image.c`, `imageext.c`, `font.c`, `freetype/`, and SDL_image/SDL_ttf integration. Verify palette creation, text metrics, Unicode handling, and all supported image formats.
5. **Audio and IO:** `mixer.c`, `_audio.py`, `_sdl3_mixer_c.c`, `rwobject.c`, music decoding, device enumeration, callbacks, format negotiation, and stream/file lifetime rules.
6. **Timing and platform features:** `time.c`, `joystick.c` platform branches, macOS/Windows/Linux-specific code, environment variables, and OpenGL context setup.
7. **Rendering extensions:**
  - [x] Port `render.c` and its Cython/Python surface to SDL3 while retaining SDL2 support.
  - [x] Port `gfxdraw` to SDL3 while retaining SDL2 support.
  - [x] Port the remaining SDL-backed optional modules currently disabled by `src_c/meson.build`. The only excluded targets are the `pygame._sdl2` bindings, which remain intentionally SDL2-only under the namespace policy.

For each module:

- [ ] Replace renamed or removed SDL calls with a compatibility wrapper or a pygame-level implementation.
- [ ] Preserve Python exceptions, return values, ownership, and reference-count behavior.
- [x] Add or update focused tests for both normal and headless operation.
- [ ] Record intentional SDL3 behavior differences and verify they are acceptable rather than masking them.

**Gate:** All intended core and optional modules build under SDL3, and the full pygame test suite passes except for explicitly documented platform/backend exclusions.

## Phase 4: Cython and Private SDL-Facing APIs

- [x] Audit `src_c/cython/pygame/_sdl2/*.pyx` and `.pxd` files for SDL2 declarations, constants, callbacks, ownership, and struct layout assumptions.
- [x] Decide whether the `_sdl2` Python namespace is retained as a compatibility namespace, supplemented by `_sdl3`, or split by build. `_sdl2` remains SDL2-only and raises an import-time error in SDL3 builds.
- [x] Port `_sdl2.audio`, `_sdl2.video`, `_sdl2.mixer`, controller, and touch bindings to the chosen policy. These bindings remain available only for SDL2; SDL3 builds do not install them.
- [x] Reconcile the existing SDL3-only `_audio.py` and `_sdl3_mixer.py` with the public pygame mixer/audio APIs and packaging rules.
- [x] Update generated stubs, type annotations, allow lists, PyInstaller hooks, Briefcase bootstrap behavior, and module documentation for the selected namespace policy. SDL2 and SDL3 stubcheck both pass; SDL3 installs only the supported native modules and filters runtime packaging to the selected SDL major.

**Gate:** Every supported SDL-facing Python import either works with tested semantics or fails early with a clear, documented exception.

## Phase 5: Test and CI Completion

- [ ] Turn `.github/workflows/build-sdl3.yml` into a real matrix covering Linux, Windows, and macOS, with pinned SDL3 companion-library versions and the same Python versions used for release builds.
- [ ] Enable the complete pygame test command under SDL3, retaining only exclusions that are genuinely unavailable in the test environment and explaining each one. A staged headless run reaches 2272 tests with one raw-install metadata failure in `version_test`; the focused SDL3 slice passes 224 tests.
- [x] Run the SDL2 and SDL3 suites from the same source revision to detect accidental regressions and behavior drift.
- [x] Add focused regression tests for renamed/removed APIs, SDL3 rectangle semantics, float mouse coordinates, audio format negotiation, IO callbacks, surface conversion, font rendering, image formats, renderer behavior, and module imports.
- [x] Add headless tests with `SDL_VIDEODRIVER=dummy` and the configured audio driver. Add a small interactive smoke test for window, event, rendering, and audio paths where CI supports it.
- [ ] Build and inspect wheels on each native platform; verify imports in a clean environment and check that runtime DLL/shared-library names match the selected SDL major version.
- [ ] Add a test that builds with `SDL_ENABLE_OLD_NAMES=0` or otherwise verifies no accidental old-name dependency remains.
- [ ] Keep the repository's standard checks green: `python -m pytest`, `python -m ruff check .`, and the calculator simulator smoke test from `AGENTS.md`.

**Gate:** SDL3 CI is as meaningful as SDL2 CI, wheels install in clean environments, and failures identify a subsystem rather than being limited to an import smoke test.

## Phase 6: Documentation and Release Transition

- [x] Update the README dependency table and build instructions for SDL2 and SDL3, including companion-library versions and platform limitations.
- [x] Document the SDL selection option and local commands, including `python dev.py build --sdl3` and the SDL3 test command.
- [x] Document public behavior differences, unavailable APIs, private namespace policy, and Emscripten status.
- [ ] Add SDL3 to release build artifacts only after native CI and wheel validation are complete. Keep SDL2 as the default until adoption and downstream compatibility are reviewed.
- [ ] Decide the default transition policy: SDL2 default with supported SDL3 opt-in, SDL3 default with SDL2 fallback, or SDL3-only. Make this a release-note and deprecation decision, not an incidental build change.
- [ ] Update version metadata, changelog/release notes, package classifiers if needed, and downstream migration guidance.
- [ ] After at least one release cycle with SDL3 support, remove obsolete SDL2-only build paths and compatibility code only when usage and support policy justify it.

**Release gate:** Documentation, wheels, tests, and support statements agree about the supported SDL API and platform matrix.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| SDL3 removes or changes an API that pygame historically exposes | Emulate it in pygame where feasible; otherwise define a tested, documented limitation. |
| SDL2 old-name aliases hide incomplete ports | Compile with old names disabled before completion and keep a source audit of SDL2 identifiers. |
| SDL companion libraries have independent API/ABI changes | Pin and test SDL3, SDL3_image, SDL3_ttf, and SDL3_mixer as a versioned set. |
| Native builds pass while Windows wheels ship the wrong DLLs | Test clean wheel installs and inspect packaged DLL/import-library names per architecture. |
| Emscripten remains SDL2-only | Give WASM its own milestone and support statement; never silently claim cross-platform SDL3 parity. |
| SDL3 behavior changes rendering, input, or audio semantics | Add behavior-focused regression tests and compare SDL2/SDL3 results where equivalence is expected. |
| Private `_sdl2` APIs create an accidental compatibility promise | Choose and document the namespace policy before porting the Cython modules. |

## Definition of Done

The SDL3 port is ready for supported release consideration when:

- all supported native platforms build and package SDL3 consistently;
- all intended pygame modules, including optional modules, are available under SDL3;
- the full test suite and focused SDL3 regressions pass with documented backend exclusions;
- the build succeeds without SDL3 old-name aliases masking unresolved calls;
- SDL2 remains green or its changed support status is explicitly approved;
- clean wheel installs, PyInstaller/Briefcase paths, and runtime library loading are verified;
- documentation and release notes state the exact SDL3 and companion-library support matrix;
- Emscripten/Pyodide status is explicit and tested if claimed as supported.
