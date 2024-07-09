import webbrowser

# use relative import here and not absolute, so that `python -m docs` works at
# development time
from . import PKG_DIR


def open_docs():
    main_page = PKG_DIR / "index.html"
    if main_page.exists():
        url = main_page.as_uri()
    else:
        url = "https://pyga.me/docs/"
    webbrowser.open(url)


def main():
    print("Opening local documentation files in the browser.")
    print(
        "If you want to run a simple server instead, run 'python -m pygame.docs.serve'."
    )
    open_docs()


if __name__ == "__main__":
    main()
