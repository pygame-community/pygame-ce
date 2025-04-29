math = py.extension_module(
    'math',
    'math.c',
    include_directories: '../include',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)
install_data('math.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
py.install_sources('math_test.py', subdir: pg / 'tests')
