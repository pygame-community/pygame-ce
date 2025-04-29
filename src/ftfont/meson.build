py.install_sources('ftfont.py', subdir: pg)
if not get_option('stripped')
    py.install_sources('ftfont_test.py', subdir: pg / 'tests')
endif

# if not building font, install use ftfont for font.py
if not sdl_ttf_dep.found() and freetype_dep.found()
    py.install_sources('ftfont.py', subdir: pg, rename: 'font.py')
endif
