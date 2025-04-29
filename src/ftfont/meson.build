py.install_sources('ftfont.py', subdir: pg)
py.install_sources('ftfont_test.py', subdir: pg / 'tests')

# if not building font, install use ftfont for font.py
if not sdl_ttf_dep.found() and freetype_dep.found()
    py.install_sources('ftfont.py', subdir: pg, rename: 'font.py')
endif
