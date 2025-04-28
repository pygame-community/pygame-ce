event = py.extension_module(
    'event',
    'event.c',
    include_directories: '..',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)
install_data('event.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
py.install_sources('event_test.py', subdir: pg / 'tests')
