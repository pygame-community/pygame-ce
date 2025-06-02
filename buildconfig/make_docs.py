#!/usr/bin/env python

import sys
import os
import subprocess
import glob

rst_dir = 'docs'
rst_source_dir = os.path.join(rst_dir, 'reST')
rst_build_dir = os.path.join('docs', 'generated')
rst_doctree_dir = os.path.join(rst_build_dir, 'doctrees')
c_header_dir = os.path.join('src_c', 'doc')


ignore_dirs = ["freetype"]


def move_doc_headers():
    for file in glob.glob(f'{c_header_dir}/*.h'):
        file_name = file.replace(c_header_dir + os.sep, '')
        module_name = file.replace('_doc.h', '').replace(c_header_dir + os.sep, '')
        if module_name not in ignore_dirs:
            args = ['src_c', module_name]
            path = os.path.join(*args)
            if os.path.exists(path):
                os.replace(file, os.path.join(path, file_name))


def run():
    full_generation_flag = False
    for argument in sys.argv[1:]:
        if argument == 'full_generation':
            full_generation_flag = True
    try:
        subprocess_args = [sys.executable, '-m', 'sphinx',
                           '-b', 'html',
                           '-d', rst_doctree_dir,
                           '-D', f'headers_dest={c_header_dir}',
                           '-D', 'headers_mkdirs=0',
                           rst_source_dir,
                           rst_build_dir, ]
        if full_generation_flag:
            subprocess_args.append('-E')
        print("Executing sphinx in subprocess with args:", subprocess_args)
        returncode = subprocess.run(subprocess_args).returncode
        if returncode != 0:
            return returncode
        move_doc_headers()
        return 0
    except Exception:
        print('---')
        print('Have you installed sphinx?')
        print('---')
        raise


if __name__ == '__main__':
    sys.exit(run())
