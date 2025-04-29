pg_camera_sources = ['_camera.c']
pg_camera_link = []
if plat == 'win'
    pg_camera_sources += 'camera_windows.c'
    # TODO: should this link logic be improved/made meson-ey?
    pg_camera_link = []
    foreach link_arg : [
        '-lMfplat',
        '-lMf',
        '-lMfuuid',
        '-lMfreadwrite',
        '-lOle32',
    ]
        if cc.has_link_argument(link_arg)
            pg_camera_link += link_arg
        endif
    endforeach
elif plat == 'linux'
    pg_camera_sources += 'camera_v4l2.c'
endif

python_sources = files(
    '_camera_opencv.py',
    'camera.py',
)

_camera = py.extension_module(
    '_camera',
    pg_camera_sources,
    include_directories: '../include',
    c_args: warnings_error,
    dependencies: pg_base_deps,
    link_args: pg_camera_link,
    install: true,
    subdir: pg,
)
install_data('camera.pyi', install_dir: pg_dir, install_tag: 'pg-tag')
py.install_sources(python_sources, subdir: pg)
py.install_sources('camera_test.py', subdir: pg / 'tests')
