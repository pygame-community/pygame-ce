py.install_sources('sndarray.py', subdir: pg)
install_data('sndarray.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
if not get_option('stripped')
    py.install_sources('sndarray_test.py', subdir: pg / 'tests')
endif
