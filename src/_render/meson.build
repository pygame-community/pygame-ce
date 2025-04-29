# TODO: support SDL3
if sdl_api != 3
_render = py.extension_module(
    '_render',
    'render.c',
    include_directories: '..',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)
endif
