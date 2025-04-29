py.install_sources('version.py', subdir: pg)
install_data('version.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
if not get_option('stripped')
    py.install_sources('version_test.py', subdir: pg / 'tests')
endif
