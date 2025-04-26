bufferproxy = py.extension_module(
    'bufferproxy',
    'bufferproxy.c',
    include_directories: '..',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)
install_data('bufferproxy.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
py.install_sources('bufferproxy_test.py', subdir: pg / 'tests')
