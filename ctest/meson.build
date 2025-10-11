unity_subproject = subproject('unity')
unity_dependency = unity_subproject.get_variable('unity_dep')

base_ctest = py.extension_module(
    'base_ctest',
    'base_ctest.c',
    c_args: warnings_error,
    dependencies: [pg_base_deps, unity_dependency],
    sources: ['../src_c/base.c'],
    install: true,
    subdir: pg,
    include_directories: ['../src_c']
)
