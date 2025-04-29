py.install_sources('_debug.py', subdir: pg)
install_data('_debug.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
if not get_option('stripped')
    py.install_sources('debug_test.py', subdir: pg / 'tests')
endif
