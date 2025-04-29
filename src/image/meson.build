image = py.extension_module(
    'image',
    'image.c',
    include_directories: '../include',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)

if sdl_image_dep.found()
    imageext = py.extension_module(
        'imageext',
        'imageext.c',
        include_directories: '../include',
        c_args: warnings_error,
        dependencies: pg_base_deps + sdl_image_dep,
        install: true,
        subdir: pg,
    )
endif

install_data('image.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
py.install_sources('image_test.py', subdir: pg / 'tests')
