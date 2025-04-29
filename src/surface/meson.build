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

    surface = py.extension_module(
        'surface',
        [
            'surface.c',
            'alphablit.c',
            'surface_fill.c',
        ],
        include_directories: '../include',
        c_args: warnings_error,
        link_with: [
            simd_blitters_avx2,
            simd_blitters_sse2,
            simd_surface_fill_avx2,
            simd_surface_fill_sse2,
        ],
        dependencies: pg_base_deps,
        install: true,
        subdir: pg,
    )
    install_data('surface.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
    if not get_option('stripped')
        py.install_sources('surface_test.py', subdir: pg / 'tests')
        py.install_sources('blit_test.py', subdir: pg / 'tests')
    endif
endif
