if fs.is_dir('generated')
    # korean tutorials are excluded for now
    install_subdir(
        'generated',
        exclude_directories: [
            'doctrees',
            'tutorials/ko',
            '_sources/tutorials/ko',
        ],
        exclude_files: ['.buildinfo', 'objects.inv'],
        install_dir: pg_dir / 'docs',
        install_tag: 'pg-tag',
    )
elif get_option('error_docs_missing')
    error('The "generated" docs folder does not exist!')
endif

docs_files = files(['__main__.py', '__init__.py', 'serve.py', 'static.py'])
py.install_sources(docs_files, subdir: pg / 'docs')
