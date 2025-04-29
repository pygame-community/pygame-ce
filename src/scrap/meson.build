pg_scrap_link = [] # TODO: should this link logic be improved/made meson-ey?
if plat == 'win'
    pg_scrap_link += ['-luser32', '-lgdi32']
endif

scrap = py.extension_module(
    'scrap',
    'scrap.c',
    include_directories: '../include',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    install: true,
    subdir: pg,
)
install_data('scrap.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
py.install_sources('scrap_test.py', subdir: pg / 'tests')
