# python -m pygame.docs.serve

import sys
import webbrowser
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

from pygame.docs import PKG_DIR, has_local_docs


class DocsHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, directory=str(PKG_DIR))


def serve(address: str, port: int):
    with ThreadingHTTPServer((address, port), DocsHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)


TARGET = "localhost"


def main():
    print("Running a simple server to serve documentation.")
    print(
        "If you want to just open documentation files in the browser, "
        "run 'python -m pygame.docs.static'."
    )
    if not has_local_docs():
        print("ERROR: no local documentation found, cannot serve anything, exiting...")
        sys.exit(1)
    print("WARNING: this is not for production use!")
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "port",
        action="store",
        default=8000,
        type=int,
        nargs="?",
        help="specify alternate port (default: 8000)",
    )
    parser.add_argument(
        "--no-browser",
        "-n",
        action="store_false",
        default=True,
        dest="open_browser",
        help="whether to open a browser tab",
    )

    parsed_args = parser.parse_args()

    print(f"Serving on: http://{TARGET}:{parsed_args.port}")

    if parsed_args.open_browser:
        webbrowser.open(f"http://{TARGET}:{parsed_args.port}")

    serve(TARGET, parsed_args.port)


if __name__ == "__main__":
    main()
