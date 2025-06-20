# first the "required" modules

# replace all instances of py.extension_module with shared_module

base = shared_module(
    'base',
    'base.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install_dir: pg,
)

color = shared_module(
    'color',
    'color.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install_dir: pg,
)

constants = shared_module(
    'constants',
    'constants.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install_dir: pg,
)

# TODO: support SDL3
if sdl_api != 3
display = shared_module(
    'display',
    'display.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install_dir: pg,
)
endif

event = shared_module(
    'event',
    'event.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install_dir: pg,
)

key = shared_module(
    'key',
    'key.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install_dir: pg,
)

mouse = shared_module(
    'mouse',
    'mouse.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install_dir: pg,
)

rect = shared_module(
    'rect',
    ['rect.c', 'pgcompat_rect.c'],
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install_dir: pg,
)

rwobject = shared_module(
    'rwobject',
    'rwobject.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install_dir: pg,
)

# TODO: support SDL3
if sdl_api != 3
simd_blitters_avx2 = static_library(
    'simd_blitters_avx2',
    'simd_blitters_avx2.c',
    dependencies: pg_base_deps,
    c_args: simd_avx2_flags + warnings_error,
)

simd_blitters_sse2 = static_library(
    'simd_blitters_sse2',
    'simd_blitters_sse2.c',
    dependencies: pg_base_deps,
    c_args: simd_sse2_neon_flags + warnings_error,
)

simd_surface_fill_avx2 = static_library(
    'simd_surface_fill_avx2',
    'simd_surface_fill_avx2.c',
    dependencies: pg_base_deps,
    c_args: simd_avx2_flags + warnings_error,
)

simd_surface_fill_sse2 = static_library(
    'simd_surface_fill_sse2',
    'simd_surface_fill_sse2.c',
    dependencies: pg_base_deps,
    c_args: simd_sse2_neon_flags + warnings_error,
)

surface = shared_module(
    'surface',
    [
        'surface.c',
        'alphablit.c',
        'surface_fill.c',
    ],
    c_args: warnings_error,
    link_with: [
        simd_blitters_avx2,
        simd_blitters_sse2,
        simd_surface_fill_avx2,
        simd_surface_fill_sse2,
    ],
    dependencies: pg_base_deps,
    install_dir: pg,
)
endif

surflock = shared_module(
    'surflock',
    'surflock.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install_dir: pg,
)

time = shared_module(
    'time',
    'time.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install_dir: pg,
)

joystick = shared_module(
    'joystick',
    'joystick.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install_dir: pg,
)

draw = shared_module(
    'draw',
    'draw.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install_dir: pg,
)

image = shared_module(
    'image',
    'image.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install_dir: pg,
)

simd_transform_avx2 = static_library(
    'simd_transform_avx2',
    'simd_transform_avx2.c',
    dependencies: pg_base_deps,
    c_args: simd_avx2_flags + warnings_error,
)

simd_transform_sse2 = static_library(
    'simd_transform_sse2',
    'simd_transform_sse2.c',
    dependencies: pg_base_deps,
    c_args: simd_sse2_neon_flags + warnings_error,
)

transform_sources = ['transform.c', 'rotozoom.c', 'scale2x.c']
transform_objs = []

if (
    cc.get_argument_syntax() == 'msvc'
    and host_machine.cpu_family().startswith('x86')
)
    if host_machine.cpu_family() == 'x86'
        transform_objs += '../buildconfig/obj/win32/scale_mmx.obj'
    else
        transform_objs += '../buildconfig/obj/win64/scale_mmx.obj'
    endif
else
    transform_sources += 'scale_mmx.c'
endif

transform = shared_module(
    'transform',
    transform_sources,
    c_args: warnings_error,
    link_with: [simd_transform_avx2, simd_transform_sse2],
    objects: transform_objs,
    dependencies: pg_base_deps,
    install_dir: pg,
)

mask = shared_module(
    'mask',
    ['mask.c', 'bitmask.c'],
    c_args: warnings_error + warnings_temp_mask,
    dependencies: pg_base_deps,
    install_dir: pg,
)

bufferproxy = shared_module(
    'bufferproxy',
    'bufferproxy.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install_dir: pg,
)

pixelarray = shared_module(
    'pixelarray',
    'pixelarray.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install_dir: pg,
)

math = shared_module(
    'math',
    'math.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install_dir: pg,
)

pixelcopy = shared_module(
    'pixelcopy',
    'pixelcopy.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install_dir: pg,
)

newbuffer = shared_module(
    'newbuffer',
    'newbuffer.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install_dir: pg,
)

# new/experimental/uncommon stuff, but built by default
system = shared_module(
    'system',
    'system.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install_dir: pg,
)

geometry = shared_module(
    'geometry',
    'geometry.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install_dir: pg,
)

window = shared_module(
    'window',
    'window.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install_dir: pg,
)

# TODO: support SDL3
if sdl_api != 3
_render = shared_module(
    '_render',
    'render.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install_dir: pg,
)
endif

# TODO: support SDL3
if sdl_api != 3
gfxdraw = shared_module(
    'gfxdraw',
    ['gfxdraw.c', 'SDL_gfx/SDL_gfxPrimitives.c'],
    # c_args: warnings_error,
    dependencies: pg_base_deps,
    install_dir: pg,
)
endif

# pygame._sdl2
# TODO: support SDL3
if sdl_api != 3
subdir('_sdl2')
endif

# pygame._camera
pg_camera_sources = ['_camera.c']
pg_camera_link = []
if plat == 'win'
    pg_camera_sources += 'camera_windows.c'
    # TODO: should this link logic be improved/made meson-ey?
    pg_camera_link = []
    foreach link_arg : [
        '-lMfplat',
        '-lMf',
        '-lMfuuid',
        '-lMfreadwrite',
        '-lOle32',
    ]
        if cc.has_link_argument(link_arg)
            pg_camera_link += link_arg
        endif
    endforeach
elif plat == 'linux'
    pg_camera_sources += 'camera_v4l2.c'
endif

_camera = shared_module(
    '_camera',
    pg_camera_sources,
    c_args: warnings_error,
    dependencies: pg_base_deps,
    link_args: pg_camera_link,
    install_dir: pg,
)

# pygame.scrap
pg_scrap_link = [] # TODO: should this link logic be improved/made meson-ey?
if plat == 'win'
    pg_scrap_link += ['-luser32', '-lgdi32']
endif

scrap = shared_module(
    'scrap',
    'scrap.c',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    link_args: pg_scrap_link,
    install_dir: pg,
)

# optional modules

if sdl_image_dep.found()
    imageext = shared_module(
        'imageext',
        'imageext.c',
        c_args: warnings_error,
        dependencies: pg_base_deps + sdl_image_dep,
        install_dir: pg,
    )
endif

if sdl_ttf_dep.found()
    font = shared_module(
        'font',
        'font.c',
        c_args: warnings_error,
        dependencies: pg_base_deps + sdl_ttf_dep,
        install_dir: pg,
    )
endif

# TODO: support SDL3
if sdl_api != 3

if sdl_mixer_dep.found()
    mixer = shared_module(
        'mixer',
        'mixer.c',
        c_args: warnings_error,
        dependencies: pg_base_deps + sdl_mixer_dep,
        install_dir: pg,
    )

    mixer_music = shared_module(
        'mixer_music',
        'music.c',
        c_args: warnings_error,
        dependencies: pg_base_deps + sdl_mixer_dep,
        install_dir: pg,
    )
endif

# if freetype_dep.found()
#     _freetype = shared_module(
#         '_freetype',
#         [
#             'freetype/ft_cache.c',
#             'freetype/ft_wrap.c',
#             'freetype/ft_render.c',
#             'freetype/ft_render_cb.c',
#             'freetype/ft_layout.c',
#             'freetype/ft_unicode.c',
#             '_freetype.c',
#         ],
#         c_args: warnings_error + warnings_temp_freetype,
#         dependencies: pg_base_deps + freetype_dep,
#         install_dir: pg,
#     )
# endif

endif

# if portmidi_dep.found()
#     pypm = shared_module(
#         'pypm',
#         fs.is_file('pypm.c') ? 'pypm.c' : 'cython/pygame/pypm.pyx',
#         # c_args: warnings_error,
#         dependencies: pg_base_deps + portmidi_deps,
#         install_dir: pg,
#     )
# endif
