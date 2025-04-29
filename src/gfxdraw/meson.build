# TODO: support SDL3
if sdl_api != 3
gfxdraw = py.extension_module(
    'gfxdraw',
    ['gfxdraw.c', 'SDL_gfxPrimitives.c'],
    include_directories: '../include',
    # c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)
install_data('gfxdraw.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
py.install_sources('gfxdraw_test.py', subdir: pg / 'tests')
endif
