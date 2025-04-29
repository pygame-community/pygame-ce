# first the "required" modules

subdir('base')

subdir('color')

subdir('constants')

subdir('display')

subdir('event')

subdir('key')

subdir('mouse')

subdir('rect')

subdir('rwobject')

subdir('surface')

subdir('surflock')

subdir('time')

subdir('joystick')

subdir('draw')

subdir('image')

subdir('transform')

subdir('mask')

subdir('bufferproxy')

subdir('pixelarray')

subdir('math')

pixelcopy = py.extension_module(
    'pixelcopy',
    'pixelcopy.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)

newbuffer = py.extension_module(
    'newbuffer',
    'newbuffer.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)

# new/experimental/uncommon stuff, but built by default
subdir('system')

subdir('geometry')

window = py.extension_module(
    'window',
    'window.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)

# TODO: support SDL3
if sdl_api != 3
_render = py.extension_module(
    '_render',
    'render.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)
endif

# TODO: support SDL3
if sdl_api != 3
gfxdraw = py.extension_module(
    'gfxdraw',
    ['gfxdraw.c', 'SDL_gfx/SDL_gfxPrimitives.c'],
    # c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)
endif

# pygame._sdl2
subdir('_sdl2')

# pygame._camera
subdir('camera')

# pygame.scrap
pg_scrap_link = [] # TODO: should this link logic be improved/made meson-ey?
if plat == 'win'
    pg_scrap_link += ['-luser32', '-lgdi32']
endif

scrap = py.extension_module(
    'scrap',
    'scrap.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    link_args: pg_scrap_link,
    install: true,
    subdir: pg,
)

# optional modules
if sdl_ttf_dep.found()
    font = py.extension_module(
        'font',
        'font.c',
        c_args: warnings_error,
        dependencies: pg_base_deps + sdl_ttf_dep,
        install: true,
        subdir: pg,
    )
endif

# TODO: support SDL3
if sdl_api != 3

if sdl_mixer_dep.found()
    mixer = py.extension_module(
        'mixer',
        'mixer.c',
        c_args: warnings_error,
        dependencies: pg_base_deps + sdl_mixer_dep,
        install: true,
        subdir: pg,
    )

    mixer_music = py.extension_module(
        'mixer_music',
        'music.c',
        c_args: warnings_error,
        dependencies: pg_base_deps + sdl_mixer_dep,
        install: true,
        subdir: pg,
    )
endif

if freetype_dep.found()
    _freetype = py.extension_module(
        '_freetype',
        [
            'freetype/ft_cache.c',
            'freetype/ft_wrap.c',
            'freetype/ft_render.c',
            'freetype/ft_render_cb.c',
            'freetype/ft_layout.c',
            'freetype/ft_unicode.c',
            '_freetype.c',
        ],
        c_args: warnings_error + warnings_temp_freetype,
        dependencies: pg_base_deps + freetype_dep,
        install: true,
        subdir: pg,
    )
endif

endif

if portmidi_dep.found()
    pypm = py.extension_module(
        'pypm',
        fs.is_file('pypm.c') ? 'pypm.c' : 'cython/pygame/pypm.pyx',
        # c_args: warnings_error,
        dependencies: pg_base_deps + portmidi_deps,
        install: true,
        subdir: pg,
    )
endif
