import platform

# use relative import here and not absolute, so that `python -m docs` works at
# development time
from .serve import main as serve
from .static import main as static


def main():
    if platform.system() == "Linux":
        serve()
    else:
        static()


if __name__ == "__main__":
    main()
