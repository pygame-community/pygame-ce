pg_simd_cpu = static_library(
    'pg_simd_cpu',
    'cpu/pg_simd_cpu.c',
    dependencies: pg_base_deps,
    include_directories: '..',
    c_args: simd_avx2_flags + simd_sse2_neon_flags + warnings_error,
)
