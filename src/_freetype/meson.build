if sdl_api != 3
    if freetype_dep.found()
        _freetype = py.extension_module(
            '_freetype',
            [
                'ft_cache.c',
                'ft_wrap.c',
                'ft_render.c',
                'ft_render_cb.c',
                'ft_layout.c',
                'ft_unicode.c',
                'freetype.c',
            ],
            include_directories: '..',
            c_args: warnings_error + warnings_temp_freetype,
            dependencies: pg_base_deps + freetype_dep,
            install: true,
            subdir: pg,
        )
        install_data('freetype.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
        py.install_sources('freetype_test.py', subdir: pg / 'tests')
    endif
endif