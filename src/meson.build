# first the "required" modules

subdir('base')

subdir('color')

subdir('constants')

# TODO: support SDL3
if sdl_api != 3
subdir('display')
endif

event = py.extension_module(
    'event',
    'event.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)

key = py.extension_module(
    'key',
    'key.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)

mouse = py.extension_module(
    'mouse',
    'mouse.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)

subdir('rect')

rwobject = py.extension_module(
    'rwobject',
    'rwobject.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)

subdir('surface')

surflock = py.extension_module(
    'surflock',
    'surflock.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)

time = py.extension_module(
    'time',
    'time.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)

joystick = py.extension_module(
    'joystick',
    'joystick.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)

subdir('draw')

image = py.extension_module(
    'image',
    'image.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)

subdir('transform')

mask = py.extension_module(
    'mask',
    ['mask.c', 'bitmask.c'],
    c_args: warnings_error + warnings_temp_mask,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)

subdir('bufferproxy')

pixelarray = py.extension_module(
    'pixelarray',
    'pixelarray.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)

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
# TODO: support SDL3
if sdl_api != 3
subdir('_sdl2')
endif

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

if sdl_image_dep.found()
    imageext = py.extension_module(
        'imageext',
        'imageext.c',
        c_args: warnings_error,
        dependencies: pg_base_deps + sdl_image_dep,
        install: true,
        subdir: pg,
    )
endif

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
