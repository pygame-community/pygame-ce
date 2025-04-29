python_sources = files(
    '_sprite.py',
    'sprite.py'
)
py.install_sources(python_sources, subdir: pg)
install_data('sprite.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
py.install_sources('sprite_test.py', subdir: pg / 'tests')
