unity_subproject = subproject('unity')
unity_dependency = unity_subproject.get_variable('unity_dep')

test_sources = files(
    ['../src_c/base.c',
    'test_base.c']
)

inc = include_directories('../src_c')

test = executable('run_ctests',
    sources: [
        test_sources,
    ],
    include_directories: [inc],
    dependencies: [unity_dependency, py_dep, sdl_dep],
    install: true,
    install_dir: pg_dir
)

# test('test', test,
#   should_fail: false)
