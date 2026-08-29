# pure python sources
python_sources = files(
    '__init__.py',
    '_camera_opencv.py',
    '_data_classes.py',
    '_debug.py',
    '_sprite.py',
    'camera.py',
    'colordict.py',
    'cursors.py',
    'freetype.py',
    'ftfont.py',
    'locals.py',
    'macosx.py',
    'midi.py',
    'pkgdata.py',
    'sprite.py',
    'surfarray.py',
    'sysfont.py',
    'typing.py',
    'version.py',
)
py.install_sources(python_sources, subdir: pg)

if sdl_api != 3
    py.install_sources('sndarray.py', subdir: pg)
endif

# if not building font, install use ftfont for font.py
if not sdl_ttf_dep.found() and freetype_dep.found()
    install_data('ftfont.py', install_dir: pg_dir, rename: 'font.py')
endif

if sdl_api == 3
    py.install_sources('_sdl3_mixer.py', subdir: pg)
    py.install_sources('_audio.py', subdir: pg)
endif

data_files = files(
    'freesansbold.ttf',
    'pygame_icon.bmp',
)
if plat == 'mac'
    data_files += 'pygame_icon_mac.bmp'
endif

install_data(data_files, install_dir: pg_dir, install_tag: 'pg-tag')

if sdl_api != 3
    subdir('_sdl2')
else
    py.install_sources(files('_sdl2/__init__.py'), subdir: pg / '_sdl2')
endif
subdir('__pyinstaller')
subdir('__briefcase')
