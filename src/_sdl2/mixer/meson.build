if sdl_mixer_dep.found()
    _sdl2_mixer = py.extension_module(
        'mixer',
        fs.is_file('mixer.c') ? 'mixer.c' : 'mixer.pyx',
        include_directories: '../../include',
        dependencies: pg_base_deps + sdl_mixer_dep,
        install: true,
        subdir: pg / '_sdl2',
    )
endif
