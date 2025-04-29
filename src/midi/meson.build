py.install_sources('midi.py', subdir: pg)
install_data('midi.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
if not get_option('stripped')
    py.install_sources('midi_test.py', subdir: pg / 'tests')
endif
