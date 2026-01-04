pg_stub_excludes = ['.flake8']

# SDL3 only!
if sdl_api != 3
    pg_stub_excludes += ['_audio.pyi']
endif

install_subdir(
    'pygame',
    exclude_files: pg_stub_excludes,
    install_dir: pg_dir,
    strip_directory: true,
    install_tag: 'pg-tag',
)
