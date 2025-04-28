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
        transform_objs += '../../buildconfig/obj/win32/scale_mmx.obj'
    else
        transform_objs += '../../buildconfig/obj/win64/scale_mmx.obj'
    endif
else
    transform_sources += 'scale_mmx.c'
endif

transform = py.extension_module(
    'transform',
    transform_sources,
    include_directories: '..',
    c_args: warnings_error,
    link_with: [simd_transform_avx2, simd_transform_sse2],
    objects: transform_objs,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)
install_data('transform.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
py.install_sources('transform_test.py', subdir: pg / 'tests')
