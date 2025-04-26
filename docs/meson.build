if fs.is_dir('generated')
    # TODO: remove everything in exclude_directories except for 'doctrees'
    install_subdir(
        'generated',
        exclude_directories: [
            'doctrees',
            '_sources/tutorials',
            '_sources/c_api',
        ],
        exclude_files: ['.buildinfo', 'objects.inv'],
        install_dir: pg_dir / 'docs',
        install_tag: 'pg-tag',
    )
elif get_option('error_docs_missing')
    error('The "generated" docs folder does not exist!')
else
    warning('The "generated" docs folder does not exist!')
endif

docs_files = files('__init__.py', '__main__.py', 'serve.py', 'static.py')
py.install_sources(docs_files, subdir: pg / 'docs')
