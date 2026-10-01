blit_avx2 = static_library(
    'blit_avx2',
    'simd/blit_avx2.c',
    dependencies: pg_base_deps,
    include_directories: ['..', '.'],
    c_args: simd_avx2_flags + warnings_error,
)

blit_sse2 = static_library(
    'blit_sse2',
    'simd/blit_sse2.c',
    dependencies: pg_base_deps,
    include_directories: ['..', '.'],
    c_args: simd_sse2_neon_flags + warnings_error,
)

fill_avx2 = static_library(
    'fill_avx2',
    'simd/fill_avx2.c',
    dependencies: pg_base_deps,
    include_directories: ['..', '.'],
    c_args: simd_avx2_flags + warnings_error,
)

fill_sse2 = static_library(
    'fill_sse2',
    'simd/fill_sse2.c',
    dependencies: pg_base_deps,
    include_directories: ['..', '.'],
    c_args: simd_sse2_neon_flags + warnings_error,
)

surface = py.extension_module(
    'surface',
    [
        'surface.c',
        'alphablit.c',
        'surface_fill.c',
    ],
    c_args: warnings_error,
    include_directories: ['..', '.', 'simd'],
    link_with: [
        blit_avx2,
        blit_sse2,
        fill_avx2,
        fill_sse2,
        pg_simd_cpu,
    ],
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)
install_data('surface.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
