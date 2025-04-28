key = py.extension_module(
    'key',
    'key.c',
    include_directories: '..',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)
install_data('key.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
py.install_sources('key_test.py', subdir: pg / 'tests')
