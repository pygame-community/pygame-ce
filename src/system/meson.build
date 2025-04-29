system = py.extension_module(
    'system',
    'system.c',
    include_directories: '../include',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)
install_data('system.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
py.install_sources('system_test.py', subdir: pg / 'tests')
