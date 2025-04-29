# TODO: support SDL3
if sdl_api != 3
cython_base = '../cython/pygame/_sdl2'

subdir('audio')

subdir('video')

subdir('controller_old')

subdir('mixer')

_sdl2_sdl2 = py.extension_module(
    'sdl2',
    fs.is_file('sdl2.c') ? 'sdl2.c' : cython_base / 'sdl2.pyx',
    dependencies: pg_base_deps,
    include_directories: '../include',
    install: true,
    subdir: pg / '_sdl2',
)

subdir('touch')

subdir('controller')

endif

subdir('window')

subdir('_sdl2')
