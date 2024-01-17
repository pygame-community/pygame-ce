# python -m pygame.docs.serve

import sys
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


if __name__ == "__main__":
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
    parsed_args = parser.parse_args()
    target = "localhost"
    print(f"Serving on: http://{target}:{parsed_args.port}")
    serve("localhost", parsed_args.port)
