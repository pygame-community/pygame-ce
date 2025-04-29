if sdl_ttf_dep.found()
    font = py.extension_module(
        'font',
        'font.c',
        include_directories: '..',
        c_args: warnings_error,
        dependencies: pg_base_deps + sdl_ttf_dep,
        install: true,
        subdir: pg,
    )
    install_data('font.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
    py.install_sources('font_test.py', subdir: pg / 'tests')
endif
