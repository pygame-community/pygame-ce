_sdl2_audio = py.extension_module(
    'audio',
    fs.is_file('audio.c') ? 'audio.c' : 'audio.pyx',
    include_directories: '../../include',
    dependencies: pg_base_deps,
    install: true,
    subdir: pg / '_sdl2',
)

install_data('audio.pyi', install_dir: pg_dir / '_sdl2', install_tag: 'pg-tag')
