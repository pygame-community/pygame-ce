rect = py.extension_module(
    'rect',
    ['rect.c', 'pgcompat_rect.c'],
    include_directories: '../include',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)
install_data('rect.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
if not get_option('stripped')
    py.install_sources('rect_test.py', subdir: pg / 'tests')
endif
