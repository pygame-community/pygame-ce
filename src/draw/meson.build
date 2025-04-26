draw = py.extension_module(
    'draw',
    'draw.c',
    include_directories: '..',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)
install_data('draw.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
py.install_sources('draw_test.py', subdir: pg / 'tests')
