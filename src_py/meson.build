# pure python sources
python_sources = files(
    '__init__.py',
    'locals.py',
    'macosx.py',
    'midi.py',
    'pkgdata.py',
    'sndarray.py',
    'surfarray.py',
    'sysfont.py',
)
py.install_sources(python_sources, subdir: pg)

# if not building font, install use ftfont for font.py
if not sdl_ttf_dep.found() and freetype_dep.found()
    py.install_sources('ftfont.py', subdir: pg, rename: 'font.py')
endif
