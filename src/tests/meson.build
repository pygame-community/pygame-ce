if not get_option('stripped')
    test_files = files(
        '__init__.py',
        '__main__.py',
    )

    py.install_sources(test_files, subdir: pg / 'tests')

    install_subdir('fixtures', install_dir: pg_dir / 'tests', install_tag: 'pg-tag')
    subdir('test_utils')
endif
