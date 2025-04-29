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

subdir('pixelcopy')

subdir('newbuffer')

# new/experimental/uncommon stuff, but built by default
subdir('system')

subdir('geometry')

subdir('window')

subdir('_render')

subdir('gfxdraw')

subdir('_sdl2')

subdir('camera')

subdir('scrap')

# optional modules
subdir('font')

subdir('mixer')

if sdl_api != 3

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
