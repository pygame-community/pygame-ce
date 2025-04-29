py.install_sources('typing.py', subdir: pg)
install_data('typing.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
if not get_option('stripped')
    py.install_sources('typing_test.py', subdir: pg / 'tests')
endif
