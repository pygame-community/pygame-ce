if sdl_api != 3
    _sdl2_sdl2 = py.extension_module(
        'sdl2',
        fs.is_file('sdl2.c') ? 'sdl2.c' : 'sdl2.pyx',
        include_directories: '../../include',
        dependencies: pg_base_deps,
        install: true,
        subdir: pg / '_sdl2',
    )
    install_data('sdl2.pyi', install_dir: pg_dir / '_sdl2', install_tag: 'pg-tag')
endif

py.install_sources('__init__.py', subdir: pg / '_sdl2')
install_data('__init__.pyi', install_dir: pg_dir / '_sdl2', install_tag: 'pg-tag')
