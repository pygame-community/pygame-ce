rwobject = py.extension_module(
    'rwobject',
    'rwobject.c',
    include_directories: '../include',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)
install_data('rwobject.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
py.install_sources('rwobject_test.py', subdir: pg / 'tests')
