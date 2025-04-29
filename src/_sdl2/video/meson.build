_sdl2_video = py.extension_module(
    'video',
    fs.is_file('video.c') ? 'video.c' : 'video.pyx',
    include_directories: '../../include',
    dependencies: pg_base_deps,
    install: true,
    subdir: pg / '_sdl2',
)

install_data('video.pyi', install_dir: pg_dir / '_sdl2', install_tag: 'pg-tag')
py.install_sources('video_test.py', subdir: pg / 'tests')