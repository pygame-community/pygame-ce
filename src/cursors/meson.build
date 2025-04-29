py.install_sources('cursors.py', subdir: pg)
install_data('cursors.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
if not get_option('stripped')
    py.install_sources('cursors_test.py', subdir: pg / 'tests')
endif
