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

subdir('typing')

subdir('sprite')

subdir('cursors')

subdir('version')

# new/experimental/uncommon stuff, but built by default
subdir('_debug')

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

subdir('ftfont')

subdir('mixer')

subdir('_freetype')

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

subdir('macosx')

subdir('resources')

subdir('__briefcase')

subdir('__pyinstaller')
