#!/usr/bin/env python

import sys
import os
import subprocess
import glob

rst_dir = 'docs'
rst_source_dir = os.path.join(rst_dir, 'reST')
rst_build_dir = os.path.join('docs', 'generated')
rst_doctree_dir = os.path.join(rst_build_dir, 'doctrees')
c_header_dir = os.path.join('src', 'doc')

special_paths = {
    "music": os.path.join("src", "mixer"),
    "pygame": os.path.join("src", "base")
}

def move_doc_headers():
    for file in glob.glob(f'{c_header_dir}/*.h'):
        file_name = file.replace(c_header_dir + os.sep, '')
        module_name = file.replace('_doc.h', '').replace(c_header_dir + os.sep, '')
        if module_name not in ['freetype']:
            args = ['src', module_name]
            if 'sdl2_' in module_name:
                module_name = module_name.replace('sdl2_', '')
                args.insert(1, 'sdl2')
            path = special_paths[module_name] if module_name in special_paths else os.path.join(*args)
            if os.path.exists(path):
                os.replace(file, os.path.join(path, file_name))
                print(f"Moved file {file_name} from {file} to {os.path.join(path, file_name)}")
            else:
                print(f"Skipping file {file} because there is no destination")

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
