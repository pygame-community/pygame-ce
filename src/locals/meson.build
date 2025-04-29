py.install_sources('locals.py', subdir: pg)
install_data('locals.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
if not get_option('stripped')
    py.install_sources('locals_test.py', subdir: pg / 'tests')
endif
