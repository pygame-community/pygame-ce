# pure python sources
test_files = files(
    '__init__.py',
    '__main__.py',
    'blit_test.py',
    'controller_test.py',
    'cursors_test.py',
    'docs_test.py',
    'ftfont_test.py',
    'image__save_gl_surface_test.py',
    'imageext_test.py',
    'locals_test.py',
    'midi_test.py',
    'sndarray_tags.py',
    'sndarray_test.py',
    'surfarray_tags.py',
    'surfarray_test.py',
    'sysfont_test.py',
    'touch_test.py',
    'video_test.py',
)

py.install_sources(test_files, subdir: pg / 'tests')

install_subdir('fixtures', install_dir: pg_dir / 'tests', install_tag: 'pg-tag')
subdir('test_utils')
