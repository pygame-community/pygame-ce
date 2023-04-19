#!/usr/bin/env python

import sys
import os
import subprocess
import shutil

rst_dir = 'docs'
rst_source_dir = os.path.join(rst_dir, 'reST')
rst_build_dir = os.path.join('docs', 'generated')
rst_doctree_dir = os.path.join(rst_build_dir, 'doctrees')
c_header_dir = os.path.join('src_c', 'doc')


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
        if returncode == 0:
            add_js_files()
        return returncode
    except Exception:
        print('---')
        print('Have you installed sphinx?')
        print('---')
        raise

def add_js_files():
    files_to_change = ['search.html', 'genindex.html']
    tag_to_find = '<div class="body" role="main">'
    tag_to_add = f'<script src="script.html"></script>'
    try:
        for file in files_to_change:
            with open(os.path.join(rst_build_dir, file),'r') as f:
                data = f.read()
                index = data.find(tag_to_find)
                if index == -1:
                    return Exception
                index += len(tag_to_find) - 1
                data = data[:index + 1] + '\n' + tag_to_add + data[index:]
            with open(os.path.join(rst_build_dir, file),'w') as f:
                f.write(data)
        original = r"{}".format(os.path.join(rst_source_dir, 'themes/classic') + '\script.html')
        target = r"{}".format(f'{rst_build_dir}\script.html')
        shutil.copyfile(original, target)
    except Exception:
        print('---')
        print('Failed to add js files')
        print('---')
        print(Exception)
        return Exception


if __name__ == '__main__':
    sys.exit(run())
