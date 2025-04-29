window = py.extension_module(
    'window',
    'window.c',
    include_directories: '..',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)
install_data('window.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
py.install_sources('window_test.py', subdir: pg / 'tests')
