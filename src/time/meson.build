time = py.extension_module(
    'time',
    'time.c',
    include_directories: '..',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)
install_data('time.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
py.install_sources('time_test.py', subdir: pg / 'tests')
