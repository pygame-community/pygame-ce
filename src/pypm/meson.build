if portmidi_dep.found()
    pypm = py.extension_module(
        'pypm',
        fs.is_file('pypm.c') ? 'pypm.c' : 'pypm.pyx',
        include_directories: '../include',
        dependencies: pg_base_deps + portmidi_deps,
        install: true,
        subdir: pg,
    )
endif
