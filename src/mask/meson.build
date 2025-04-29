mask = py.extension_module(
    'mask',
    ['mask.c', 'bitmask.c'],
    include_directories: '../include',
    c_args: warnings_error + warnings_temp_mask,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)
install_data('mask.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
if not get_option('stripped')
    py.install_sources('mask_test.py', subdir: pg / 'tests')
endif
