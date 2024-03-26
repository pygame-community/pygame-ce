_sdl2_audio = py.extension_module(
    'audio',
    'audio.c',
    dependencies: pg_base_deps,
    include_directories: '..',
    install: true,
    subdir: pg / '_sdl2',
)

_sdl2_video = py.extension_module(
    'video',
    'video.c',
    dependencies: pg_base_deps,
    include_directories: '..',
    install: true,
    subdir: pg / '_sdl2',
)

_sdl2_controller_old = py.extension_module(
    'controller_old',
    'controller_old.c',
    dependencies: pg_base_deps,
    include_directories: '..',
    install: true,
    subdir: pg / '_sdl2',
)

if sdl_mixer_dep.found()
    _sdl2_mixer = py.extension_module(
        'mixer',
        'mixer.c',
        dependencies: pg_base_deps + sdl_mixer_dep,
        include_directories: '..',
        install: true,
        subdir: pg / '_sdl2',
    )
endif

_sdl2_sdl2 = py.extension_module(
    'sdl2',
    'sdl2.c',
    dependencies: pg_base_deps,
    include_directories: '..',
    install: true,
    subdir: pg / '_sdl2',
)

_sdl2_touch = py.extension_module(
    'touch',
    'touch.c',
    dependencies: pg_base_deps,
    include_directories: '..',
    install: true,
    subdir: pg / '_sdl2',
)
