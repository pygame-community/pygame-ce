constants = py.extension_module(
    'constants',
    'constants.c',
    include_directories: '..',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)
install_data('constants.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
py.install_sources('constants_test.py', subdir: pg / 'tests')
