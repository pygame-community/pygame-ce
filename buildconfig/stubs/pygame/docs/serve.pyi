from http.server import SimpleHTTPRequestHandler


class DocsHandler(SimpleHTTPRequestHandler): ...


def serve(address: str, port: str): ...


def main(): ...


TARGET: str
