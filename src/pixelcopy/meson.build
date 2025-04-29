pixelcopy = py.extension_module(
    'pixelcopy',
    'pixelcopy.c',
    include_directories: '../include',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)
install_data('pixelcopy.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
py.install_sources('pixelcopy_test.py', subdir: pg / 'tests')
