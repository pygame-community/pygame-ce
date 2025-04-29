py.install_sources('surfarray.py', subdir: pg)
install_data('surfarray.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
if not get_option('stripped')
    py.install_sources('surfarray_test.py', subdir: pg / 'tests')
endif
