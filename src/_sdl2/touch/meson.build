_sdl2_touch = py.extension_module(
    'touch',
    'touch.c',
    dependencies: pg_base_deps,
    include_directories: '../../include',
    install: true,
    subdir: pg / '_sdl2',
)

install_data('touch.pyi', install_dir: pg_dir / '_sdl2', install_tag: 'pg-tag')
py.install_sources('touch_test.py', subdir: pg / 'tests')
