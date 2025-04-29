newbuffer = py.extension_module(
    'newbuffer',
    'newbuffer.c',
    include_directories: '../include',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)
