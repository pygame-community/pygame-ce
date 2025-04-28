display = py.extension_module(
    'display',
    'display.c',
    include_directories: '..',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)
install_data('display.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
py.install_sources('display_test.py', subdir: pg / 'tests')
