unity_subproject = subproject('unity')
unity_dependency = unity_subproject.get_variable('unity_dep')

test_sources = files(
    '../src_c/base.c',
    'test_base.c'
)

inc = include_directories('../src_c')

py_version = py.language_version().split('.')
py_major = py_version[0]
py_minor = py_version[1]
libpython_name = 'python' + py_major + '.' + py_minor

libpython = cc.find_library(libpython_name, required: false)

python_dep = dependency(libpython_name, required: false)
if not python_dep.found()
    python_dep = declare_dependency(
        dependencies: libpython
    )
endif

executable('run_ctests',
    sources: [
        test_sources,
    ],
    include_directories: [inc],
    dependencies: [unity_dependency, sdl_dep, python_dep, py_dep],
    install: true,
    install_dir: pg_dir
)
