import logging
from scripts.download import main as download_main
from scripts.extract_zip import main as extract_main
from scripts.build import main as build_main
from scripts.clean import main as clean_main
from scripts.pack import main as pack_main

logging.basicConfig(force=True,level=logging.INFO, format="[%(levelname)s][%(name)s]: %(message)s")
logger = logging.getLogger("Generate")

def main(x86=True,x64=True):
    download_main()
    if x64:
        extract_main('x64')
    if x86:
        extract_main('x86')

    logger.info("Generate start.")

    pack_main("clear")
    if x64:
        clean_main()
        build_main("x64")
        pack_main("libx64")
    if x86:
        clean_main()
        build_main("x86")
        pack_main("libx86")
    pack_main("include")
    pack_main("license")

    if x64:
        pack_main("unzip",arch="x64")
    if x86:
        pack_main("unzip",arch="x86")

    logger.info("Generated successfully.")

if __name__=="__main__":
    import sys
    import platform
    if "--x64" in sys.argv:
        arch="64bit"
    elif "--x86" in sys.argv:
        arch="32bit"
    else:
        arch=platform.architecture()[0]

    if arch=="64bit":
        main(x64=True,x86=False)
    elif arch=="32bit":
        main(x64=False,x86=True)
    else:
        raise RuntimeError("Unknonw arch")
