_sdl2_controller = py.extension_module(
    'controller',
    'controller.c',
    include_directories: '../../include',
    dependencies: pg_base_deps,
    install: true,
    subdir: pg / '_sdl2',
)

install_data('controller.pyi', install_dir: pg_dir / '_sdl2', install_tag: 'pg-tag')
py.install_sources('controller_test.py', subdir: pg / 'tests')
