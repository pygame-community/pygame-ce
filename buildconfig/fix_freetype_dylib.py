import os
import shutil
import zipfile

os.chdir("../wheelhouse")

for file in os.listdir("."):
    if not file.endswith(".whl"):
        continue

    os.mkdir("extract")

    with zipfile.ZipFile(file) as f:
        f.extractall('./extract')

    os.chdir("extract")

    # What is this doing?
    # So.
    # dlopen() on MacOS 10 and 11 appears to fail when a dynamic library tries
    # to load itself as one of its dependencies. You can see dynamic library
    # links with otool -L xxx.dylib, and you can change things with
    # install_name_tool. But why is the freetype dylib trying to load itself?
    # This is likely a bug in cibuildwheel/auditwheel/delocate?
    #
    # Anyways, this hacky solution creates a "libpaidtype" dylib, convinces it
    # is actually "libpaidtype", and then makes libfreetype link to it, 
    # avoiding the bug in dlopen.

    os.system("cp pygame/.dylibs/libfreetype.6.dylib pygame/.dylibs/libpaidtype.6.dylib")
    os.system("install_name_tool -id /DLC/pygame/.dylibs/libpaidtype.6.dylib pygame/.dylibs/libpaidtype.6.dylib")
    os.system("install_name_tool -change @loader_path/libfreetype.6.dylib @loader_path/libpaidtype.6.dylib pygame/.dylibs/libfreetype.6.dylib")

    file_namever = "-".join(file.split("-")[:2])
    print(file_namever)

    os.system(f"zip -r {file} pygame {file_namever}.data {file_namever}.dist-info")

    os.system(f"cp {file} ../{file}")

    os.chdir("..")

    shutil.rmtree("extract", ignore_errors=True)
