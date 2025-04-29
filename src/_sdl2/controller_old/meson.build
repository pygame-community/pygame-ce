_sdl2_controller_old = py.extension_module(
    'controller_old',
    fs.is_file('controller_old.c') ? 'controller_old.c' : 'controller_old.pyx',
    include_directories: '../../include',
    dependencies: pg_base_deps,
    install: true,
    subdir: pg / '_sdl2',
)

install_data('controller_old.pyi', install_dir: pg_dir / '_sdl2', install_tag: 'pg-tag')
