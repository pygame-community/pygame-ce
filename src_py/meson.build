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
    'typing.py',
    'version.py',
)
py.install_sources(python_sources, subdir: pg)

# if not building font, install use ftfont for font.py
if not sdl_ttf_dep.found() and freetype_dep.found()
    py.install_sources('ftfont.py', subdir: pg, rename: 'font.py')
endif

data_files = files(
    'freesansbold.ttf',
    'pygame_icon.bmp',
)
if plat == 'mac'
    data_files += 'pygame_icon_mac.bmp'
endif

install_data(data_files, install_dir: pg_dir, install_tag: 'pg-tag')
