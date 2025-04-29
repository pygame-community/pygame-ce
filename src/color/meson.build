color = py.extension_module(
    'color',
    'color.c',
    include_directories: '../include',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)
py.install_sources('colordict.py', subdir: pg)
install_data('color.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
if not get_option('stripped')
    py.install_sources('color_test.py', subdir: pg / 'tests')
endif
