# python -m pygame.docs

from pathlib import Path


PKG_DIR = Path(__file__).absolute().parent / "generated"


# for test suite to confirm pygame-ce built with local docs
def has_local_docs():
    return PKG_DIR.exists()
