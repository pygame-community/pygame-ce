pixelarray = py.extension_module(
    'pixelarray',
    'pixelarray.c',
    include_directories: '../include',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)
install_data('pixelarray.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
if not get_option('stripped')
    py.install_sources('pixelarray_test.py', subdir: pg / 'tests')
endif
