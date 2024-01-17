# python -m pygame.docs

from pathlib import Path
import webbrowser


PKG_DIR = Path(__file__).absolute().parent / "generated"


# for test suite to confirm pygame-ce built with local docs
def has_local_docs():
    return PKG_DIR.exists()


def open_docs():
    main_page = PKG_DIR / "index.html"
    if main_page.exists():
        url = main_page.as_uri()
    else:
        url = "https://pyga.me/docs/"
    webbrowser.open(url)
