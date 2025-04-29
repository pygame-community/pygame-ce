geometry = py.extension_module(
    'geometry',
    'geometry.c',
    include_directories: '../include',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)
install_data('geometry.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
py.install_sources('geometry_test.py', subdir: pg / 'tests')
