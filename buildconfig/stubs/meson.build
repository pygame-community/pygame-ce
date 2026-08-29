pg_stub_excludes = ['.flake8', '__init__sdl3.pyi']
pg_stub_exclude_directories = []

if sdl_api != 3
    pg_stub_excludes += ['_audio.pyi', '_sdl3_mixer.pyi']
else
    pg_stub_excludes += ['__init__.pyi']
    pg_stub_exclude_directories += ['_sdl2']
    install_data(
        'pygame/__init__sdl3.pyi',
        install_dir: pg_dir,
        rename: '__init__.pyi',
        install_tag: 'pg-tag',
    )
endif

install_subdir(
    'pygame',
    exclude_files: pg_stub_excludes,
    exclude_directories: pg_stub_exclude_directories,
    install_dir: pg_dir,
    strip_directory: true,
    install_tag: 'pg-tag',
)
