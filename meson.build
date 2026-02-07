project(
    'pygame_ce',
    ['c', 'cython'], # Project type. We need a C compiler and cython
    version: run_command(
        [find_program('python3', 'python'), 'buildconfig/get_version.py'],
        check: true,
    ).stdout().strip(),
    default_options: [
        # the warning level is set in code below, gives more flexibility there
        'warning_level=0',
    ],
)

defines = run_command(
    [find_program('python3', 'python'), 'buildconfig/get_version.py', '--macros'],
    check: true,
).stdout().strip().split()
foreach define : defines
    add_global_arguments(define, language: 'c')
endforeach

pg = 'pygame' # python base package name

if host_machine.system() == 'windows'
    plat = 'win'
elif host_machine.system() == 'darwin'
    plat = 'mac'
elif host_machine.system() == 'linux'
    plat = 'linux'
elif host_machine.system() == 'android'
    plat = 'android'
    error(
        'The meson buildconfig of pygame-ce does not support android for now.',
        'However it may be added in the future',
    )
elif host_machine.system() == 'emscripten'
    plat = 'emscripten-@0@'.format(get_option('emscripten_type'))
else
    # here it one of: cygwin, dragonfly, freebsd, gnu, haiku, netbsd, openbsd, sunos
    plat = 'unix'
    warning(
        'pygame-ce does not actively support building on your platform:',
        host_machine.system(),
    )
endif

cc = meson.get_compiler('c')

fs = import('fs')

py = import('python').find_installation(pure: false)
py_dep = py.dependency()

is_pypy = py.get_variable('implementation_lower', '') == 'pypy'

if not cc.has_header('Python.h', dependencies: py_dep)
    error(
        'Cannot use `Python.h`. Perhaps you need to install python-dev|python-devel',
    )
endif

if get_option('coverage')
    if cc.has_argument('--coverage')
        add_global_arguments('--coverage', language: 'c')
    else
        error('Requested coverage but compiler doesn\'t seem to support it')
    endif
    if cc.has_link_argument('--coverage')
        add_global_link_arguments('--coverage', language: 'c')
    else
        error('Requested coverage but compiler doesn\'t seem to support it')
    endif
endif

pg_dir = py.get_install_dir() / pg

sdl_api = get_option('sdl_api')
sdl = 'SDL@0@'.format(sdl_api)
sdl_mixer = '@0@_mixer'.format(sdl)
sdl_ttf = '@0@_ttf'.format(sdl)
sdl_image = '@0@_image'.format(sdl)

if sdl_api == 3
    add_global_arguments('-DPG_SDL3=1', '-DSDL_ENABLE_OLD_NAMES=1', language: 'c')
endif

pg_inc_dirs = []
pg_lib_dirs = []

if plat == 'emscripten-pygbag'
    sdl_dep = declare_dependency(
        link_args: ['-lSDL2'],
    )
    sdl_image_dep = declare_dependency(
        link_args: ['-lSDL2_image'],
    )
    sdl_mixer_dep = declare_dependency(
        link_args: ['-lSDL2_mixer_ogg', '-logg', '-lvorbis'],
    )
    freetype_dep = declare_dependency(
        link_args: ['-lfreetype', '-lharfbuzz']
    )
    sdl_ttf_dep = declare_dependency(
        link_args: ['-lSDL2_ttf'],
        dependencies: [freetype_dep]
    )
elif plat == 'emscripten-pyodide'
    # Check out before-build attribute in [tool.cibuildwheel.pyodide] section
    # of pyproject.toml to see how these dependencies were installed.
    wasm_exceptions = ['-fwasm-exceptions', '-sSUPPORT_LONGJMP=wasm', '-sRELOCATABLE=1']
    add_global_arguments(wasm_exceptions, language: 'c')
    add_global_link_arguments(wasm_exceptions, language: 'c')

    sdl_flags = ['-sUSE_SDL=2']
    freetype_flags = ['-sUSE_FREETYPE=1']
    sdl_dep = declare_dependency(
        compile_args: sdl_flags,
        link_args: sdl_flags + ['-lSDL2', '-lhtml5'],
    )
    sdl_image_dep = declare_dependency(
        link_args: [
            '-lSDL2_image-bmp-gif-jpg-lbm-pcx-png-pnm-qoi-svg-tga-xcf-xpm-xv-wasm-sjlj',
            '-ljpeg',
            '-lpng-legacysjlj',
        ],
    )
    sdl_mixer_dep = declare_dependency(
        link_args: [
            '-lSDL2_mixer-mid-mod-mp3-ogg',
            '-lmodplug',
            '-lmpg123',
            '-logg',
            '-lvorbis'
        ],
    )
    freetype_dep = declare_dependency(
        compile_args: freetype_flags,
        link_args: freetype_flags + ['-lfreetype-legacysjlj', '-lharfbuzz']
    )
    sdl_ttf_dep = declare_dependency(
        link_args: ['-lSDL2_ttf'],
        dependencies: [freetype_dep]
    )
else

if plat == 'win'
    # yes, this is a bit ugly and hardcoded but it is what it is
    # TODO (middle-term goal) - Should migrate away from this
    # consider meson wraps? Hopefully can also get the same build path as below

    base_dir = meson.current_source_dir()
    prebuilt_dir = base_dir / 'pygame_win_deps_' + host_machine.cpu_family()

    dlls = []

    # Here we first try the new prebuilts that CI makes available. If its not available
    # we fallback to legacy prebuilts if we are on intel/AMD, or do a system search for
    # the deps on other platforms.
    if fs.is_dir(prebuilt_dir)
        lib_dir = prebuilt_dir / 'lib'

        # These are all the dlls that we need. There are no extra DLLs here.
        dlls += [
            lib_dir / 'SDL2.dll',
            lib_dir / 'SDL2_image.dll',
            lib_dir / 'SDL2_mixer.dll',
            lib_dir / 'SDL2_ttf.dll',
            lib_dir / 'libFLAC.dll',
            lib_dir / 'libbrotlicommon.dll',
            lib_dir / 'libbrotlidec.dll',
            lib_dir / 'libfluidsynth-3.dll',
            lib_dir / 'libfreetype-6.dll',
            lib_dir / 'libharfbuzz-0.dll',
            lib_dir / 'libjpeg-62.dll',
            lib_dir / 'libopus-0.dll',
            lib_dir / 'libopusfile-0.dll',
            lib_dir / 'libpng16.dll',
            lib_dir / 'libportmidi.dll',
            lib_dir / 'libsharpyuv.dll',
            lib_dir / 'libsndfile.dll',
            lib_dir / 'libtiff.dll',
            lib_dir / 'libvorbis.dll',
            lib_dir / 'libvorbisenc.dll',
            lib_dir / 'libvorbisfile.dll',
            lib_dir / 'libwavpack-1.dll',
            lib_dir / 'libwebp.dll',
            lib_dir / 'libwebpdemux.dll',
            lib_dir / 'libwinpthread-1.dll',
            lib_dir / 'libxmp.dll',
            lib_dir / 'libzlib.dll',
            lib_dir / 'ogg.dll',
        ]
        # Because of some build time issues, libmpg123 DLL is only available on
        # x86/AMD64 and not available on ARM64.
        # However, it still works out at runtime because SDL_mixer statically
        # links against libmpg123 on ARM64.
        if host_machine.cpu_family().startswith('x86')
            dlls += lib_dir / 'libmpg123-0.dll'
        endif
        # On x86 and x64 we need to include the correct mingw libgcc dll.
        # On arm64 mingw uses clang and things are statically linked against
        # compiler-rt (so, no dll needed there)
        if host_machine.cpu_family() == 'x86'
            dlls += lib_dir / 'libgcc_s_dw2-1.dll'
        elif host_machine.cpu_family() == 'x86_64'
            dlls += lib_dir / 'libgcc_s_seh-1.dll'
        endif

        pg_inc_dirs += fs.relative_to(prebuilt_dir / 'include', base_dir)
        pg_inc_dirs += fs.relative_to(prebuilt_dir / 'include' / 'SDL2', base_dir)
        pg_inc_dirs += fs.relative_to(prebuilt_dir / 'include' / 'freetype2', base_dir)
        pg_lib_dirs += lib_dir
    elif host_machine.cpu_family().startswith('x86')
        warning('Missing windows prebuilts. Falling back to legacy prebuilts')

        sdl_ver = (sdl_api == 3) ? '3.4.0' : '2.32.10'
        sdl_image_ver = (sdl_api == 3) ? '3.4.0' : '2.8.8'
        sdl_mixer_ver = '2.8.1'
        sdl_ttf_ver = (sdl_api == 3) ? '3.2.2' : '2.24.0'

        arch_suffix = 'x' + host_machine.cpu_family().substring(-2)
        prebuilt_dir = base_dir / 'prebuilt-' + arch_suffix

        sdl_dir = prebuilt_dir / '@0@-@1@'.format(sdl, sdl_ver)
        sdl_image_dir = prebuilt_dir / '@0@-@1@'.format(sdl_image, sdl_image_ver)
        sdl_mixer_dir = prebuilt_dir / '@0@-@1@'.format(sdl_mixer, sdl_mixer_ver)
        sdl_ttf_dir = prebuilt_dir / '@0@-@1@'.format(sdl_ttf, sdl_ttf_ver)
        common_lib_dir = prebuilt_dir / 'lib'

        # download prebuilts (uses legacy buildconfig code)
        required_dirs = [
            prebuilt_dir,
            sdl_dir,
            sdl_image_dir,
            sdl_mixer_dir,
            sdl_ttf_dir,
            common_lib_dir,
        ]
        any_missing = false
        foreach d : required_dirs
            if not fs.is_dir(d)
                any_missing = true
                break
            endif
        endforeach
        if any_missing
            run_command(
                [
                    find_program('python3', 'python'),
                    'buildconfig/download_win_prebuilt.py',
                ],
                check: true,
            )
        endif

        # SDL
        sdl_lib_dir = sdl_dir / 'lib' / arch_suffix
        pg_inc_dirs += fs.relative_to(sdl_dir / 'include', base_dir)
        pg_lib_dirs += sdl_lib_dir
        dlls += sdl_lib_dir / '@0@.dll'.format(sdl)

        # SDL_image
        if get_option('image').enabled()
            sdl_image_lib_dir = sdl_image_dir / 'lib' / arch_suffix
            pg_inc_dirs += fs.relative_to(sdl_image_dir / 'include', base_dir)
            pg_lib_dirs += sdl_image_lib_dir
            dlls += [
                sdl_image_lib_dir / '@0@.dll'.format(sdl_image),
                sdl_image_lib_dir / 'optional' / (sdl_api == 3 ? 'libtiff-6.dll' : 'libtiff-5.dll'),
                sdl_image_lib_dir / 'optional' / 'libwebp-7.dll',
                sdl_image_lib_dir / 'optional' / 'libwebpdemux-2.dll',
            ]
            # temporary solution to get things compiling under SDL3_image. In the future
            # we would want to have libpng and libjpeg on SDL3_image as well.
            if sdl_api != 3
                dlls += [
                    sdl_image_lib_dir / 'optional' / 'libjpeg-62.dll',
                    sdl_image_lib_dir / 'optional' / 'libpng16-16.dll',
                ]
            endif
        endif

        # SDL_mixer
        if get_option('mixer').enabled()
            sdl_mixer_lib_dir = sdl_mixer_dir / 'lib' / arch_suffix
            pg_inc_dirs += fs.relative_to(sdl_mixer_dir / 'include', base_dir)
            pg_lib_dirs += sdl_mixer_lib_dir
            dlls += [
                sdl_mixer_lib_dir / '@0@.dll'.format(sdl_mixer),
                sdl_mixer_lib_dir / 'optional' / 'libogg-0.dll',
                sdl_mixer_lib_dir / 'optional' / 'libopus-0.dll',
                sdl_mixer_lib_dir / 'optional' / 'libopusfile-0.dll',
                sdl_mixer_lib_dir / 'optional' / 'libwavpack-1.dll',
                sdl_mixer_lib_dir / 'optional' / 'libxmp.dll',
            ]
        endif

        # SDL_ttf
        if get_option('font').enabled()
            sdl_ttf_lib_dir = sdl_ttf_dir / 'lib' / arch_suffix
            pg_inc_dirs += fs.relative_to(sdl_ttf_dir / 'include', base_dir)
            pg_lib_dirs += sdl_ttf_lib_dir
            dlls += sdl_ttf_lib_dir / '@0@.dll'.format(sdl_ttf)
        endif

        # freetype, portmidi and porttime
        if get_option('freetype').enabled() and get_option('midi').enabled()
            pg_inc_dirs += fs.relative_to(prebuilt_dir / 'include', base_dir)
            pg_lib_dirs += common_lib_dir
            dlls += [common_lib_dir / 'freetype.dll', common_lib_dir / 'portmidi.dll']
        endif

        # clean unneeded file that causes build issues
        unneeded_file = common_lib_dir / 'libportmidi.dll.a'
        if fs.exists(unneeded_file)
            run_command(
                [
                    find_program('python3', 'python'),
                    '-c',
                    'import os; os.remove("@0@")'.format(unneeded_file),
                ],
                check: true,
            )
        endif
    else
        warning(
            'Prebuilt deps weren\'t found for this system (@0@).'.format(host_machine.cpu_family()) +
            'Meson-based dependency detection will be used to resolve them from your system.'
        )
    endif

    run_command(
        [
            find_program('python3', 'python'),
            base_dir / 'buildconfig' / '_meson_win_dll.py',
            dlls,
        ],
        check: true,
    )

    foreach lib : dlls
        if not fs.exists(lib)
            error(f'''
            File "@lib@" does not exist.
            Please try to delete windows prebuilts and retry the installation.
            ''')
        endif
    endforeach

    # put dlls in root of install
    install_data(dlls, install_dir: pg_dir, install_tag: 'pg-tag')

else
    homebrew_prefix = '/opt/homebrew'

    brew_cmd = find_program('brew', required: false)

    if brew_cmd.found()
        result = run_command(brew_cmd, '--prefix', check: false)
        if result.returncode() == 0
            detected_prefix = result.stdout().strip()
            if detected_prefix != '' and fs.is_dir(detected_prefix)
                homebrew_prefix = detected_prefix
            endif
        endif
    endif

    bases = ['/usr/local', '/usr', homebrew_prefix, '/opt/local']
    foreach inc_dir : bases
        foreach sub_inc : [
            '',
            '/@0@'.format(sdl),
            '/freetype2',
        ]
            full_inc = inc_dir / 'include' + sub_inc
            if fs.exists(full_inc)
                pg_inc_dirs += full_inc
            endif
        endforeach
    endforeach

    foreach lib_dir : bases
        foreach sub_lib : ['lib', 'lib64']
            full_lib = lib_dir / sub_lib
            if fs.exists(full_lib)
                pg_lib_dirs += full_lib
            endif
        endforeach
    endforeach
endif

# TODO: add version constraints?
sdl_dep = dependency(sdl, required: false)
if not sdl_dep.found()
    sdl_dep = declare_dependency(
        include_directories: pg_inc_dirs,
        dependencies: cc.find_library(sdl, dirs: pg_lib_dirs),
    )
endif

# optional
sdl_image_dep = dependency(sdl_image, required: false)
if not sdl_image_dep.found()
    sdl_image_dep = declare_dependency(
        include_directories: pg_inc_dirs,
        dependencies: cc.find_library(
            sdl_image,
            dirs: pg_lib_dirs,
            required: get_option('image'),
        ),
    )
endif

sdl_mixer_dep = dependency(sdl_mixer, required: false)
if not sdl_mixer_dep.found()
    sdl_mixer_dep = declare_dependency(
        include_directories: pg_inc_dirs,
        dependencies: cc.find_library(
            sdl_mixer,
            dirs: pg_lib_dirs,
            required: get_option('mixer'),
        ),
    )
endif

sdl_ttf_dep = dependency(sdl_ttf, required: false)
if not sdl_ttf_dep.found()
    sdl_ttf_dep = declare_dependency(
        include_directories: pg_inc_dirs,
        dependencies: cc.find_library(
            sdl_ttf,
            dirs: pg_lib_dirs,
            required: get_option('font'),
        ),
    )
endif

freetype_dep = dependency('freetype2', required: false)
if not freetype_dep.found()
    freetype_dep = declare_dependency(
        include_directories: pg_inc_dirs,
        dependencies: cc.find_library(
            'freetype',
            dirs: pg_lib_dirs,
            required: get_option('freetype'),
        ),
    )
endif

endif # emscripten

portmidi_dep = dependency('portmidi', required: false)
if not portmidi_dep.found() and not plat.startswith('emscripten')
    portmidi_dep = declare_dependency(
        include_directories: pg_inc_dirs,
        dependencies: cc.find_library(
            'portmidi',
            dirs: pg_lib_dirs,
            required: get_option('midi'),
        ),
    )
endif

portmidi_deps = [portmidi_dep]

if portmidi_dep.found()
    # porttime can be a separate library, or be inbuilt in portmidi.
    # So if it is available as a separate library, include it as a dependency
    porttime_dep = dependency('porttime', required: false)
    if not porttime_dep.found()
        porttime_dep = cc.find_library(
            'porttime',
            dirs: pg_lib_dirs,
            required: false,
        )
    endif

    if porttime_dep.found()
        portmidi_deps += porttime_dep
    endif
endif

pg_base_deps = [sdl_dep, py_dep]

summary(
    {
        sdl: sdl_dep.found(),
        sdl_image: sdl_image_dep.found(),
        sdl_mixer: sdl_mixer_dep.found(),
        sdl_ttf: sdl_ttf_dep.found(),
        'freetype2': freetype_dep.found(),
        'portmidi': portmidi_dep.found(),
        'porttime': portmidi_dep.found() ? porttime_dep.found() : false,
    },
    section: 'Dependencies',
)

simd_avx2 = false
simd_avx2_flags = []
if host_machine.cpu_family().startswith('x86')
    flag = (cc.get_argument_syntax() == 'msvc') ? '/arch:AVX2' : '-mavx2'
    if cc.has_argument(flag)
        simd_avx2_flags += flag
        simd_avx2 = true
    endif
endif

simd_sse2_neon = false
simd_sse2_neon_flags = []
if host_machine.cpu_family() == 'arm'
    # first check if compiler supports the flag, and use it then. Needed only
    # on 32-bit armv7.
    flag = '-mfpu=neon'
    if cc.has_argument(flag) and host_machine.cpu() == 'armv7l'
        simd_sse2_neon_flags += [flag, '-march=armv7-a']
        simd_sse2_neon = true
    endif
elif host_machine.cpu_family() == 'aarch64'
    # sse2neon doesn't support compiling under msvc
    simd_sse2_neon = cc.get_id() != 'msvc'
endif

if simd_sse2_neon
    add_global_arguments('-DPG_ENABLE_ARM_NEON=1', language: 'c')
endif

summary(
    {
        'AVX2': simd_avx2,
        'NEON': simd_sse2_neon,
    },
    section: 'SIMD',
)

# stores werror
warnings_error = []

# module specific warnings (TODO remove these by fixing code)
warnings_temp_freetype = []
warnings_temp_mask = []

if cc.get_argument_syntax() == 'msvc'
    # base warnings on msvc
    add_global_arguments(['/W3', '/wd4142', '/wd4996'], language: 'c')

    warnings_temp_mask += ['/wd6385', '/wd6386']

    if get_option('error_on_warns') and not is_pypy
        warnings_error += '/WX'
    endif
    # TODO: msvc analyzer?
else
    # base warnings on gcc/clang
    add_global_arguments(['-Wall', '-Wno-error=unknown-pragmas'], language: 'c')

    # check for exact gcc (flags not needed on clang)
    if cc.get_id() == 'gcc'
        warnings_temp_freetype += [
            '-Wno-error=unused-but-set-variable',
            '-Wno-error=array-bounds',
        ]
        warnings_temp_mask += '-Wno-error=array-bounds'
    endif

    if cc.sizeof('long') != 8
        warnings_temp_mask += '-Wno-error=shift-count-overflow'
    endif

    if get_option('error_on_warns') and not is_pypy
        warnings_error += '-Werror'
    endif
endif

subdir('src_c')
subdir('src_py')

if not get_option('stripped') and not plat.startswith('emscripten')
    # run make_docs and make docs
    if not fs.is_dir('docs/generated')
        make_docs = files('buildconfig/make_docs.py')
        res = run_command(
            [find_program('python3', 'python'), make_docs],
            check: false,
        )
        message(res.stdout().strip())
        message(res.stderr().strip())
    endif
    subdir('docs')
    subdir('test')
    subdir('buildconfig/stubs')
    install_subdir('examples', install_dir: pg_dir, install_tag: 'pg-tag')
    # TODO: install headers? not really important though
endif
