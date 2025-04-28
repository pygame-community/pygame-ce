joystick = py.extension_module(
    'joystick',
    'joystick.c',
    include_directories: '..',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)
install_data('joystick.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
py.install_sources('joystick_test.py', subdir: pg / 'tests')
