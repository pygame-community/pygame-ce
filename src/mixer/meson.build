# TODO: support SDL3
if sdl_api != 3
    if sdl_mixer_dep.found()
        mixer = py.extension_module(
            'mixer',
            'mixer.c',
            include_directories: '../include',
            c_args: warnings_error,
            dependencies: pg_base_deps + sdl_mixer_dep,
            install: true,
            subdir: pg,
        )
        install_data('mixer.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
        py.install_sources('mixer_test.py', subdir: pg / 'tests')

        mixer_music = py.extension_module(
            'mixer_music',
            'music.c',
            include_directories: '../include',
            c_args: warnings_error,
            dependencies: pg_base_deps + sdl_mixer_dep,
            install: true,
            subdir: pg,
        )
        install_data('mixer_music.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
        py.install_sources('mixer_music_test.py', subdir: pg / 'tests')
    endif
endif
