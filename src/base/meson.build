base = py.extension_module(
    'base',
    'base.c',
    include_directories: '..',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)
install_data('base.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
py.install_sources('base_test.py', subdir: pg / 'tests')
