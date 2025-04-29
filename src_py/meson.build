# pure python sources
python_sources = files(
    '__init__.py',
    '_data_classes.py',
    '_debug.py',
    '_sprite.py',
    'colordict.py',
    'cursors.py',
    'freetype.py',
    'ftfont.py',
    'locals.py',
    'macosx.py',
    'midi.py',
    'pkgdata.py',
    'sndarray.py',
    'sprite.py',
    'surfarray.py',
    'sysfont.py',
    'version.py',
)
py.install_sources(python_sources, subdir: pg)

# if not building font, install use ftfont for font.py
if not sdl_ttf_dep.found() and freetype_dep.found()
    py.install_sources('ftfont.py', subdir: pg, rename: 'font.py')
endif
