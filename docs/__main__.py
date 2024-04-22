import platform

from pygame.docs.serve import main as serve
from pygame.docs.static import main as static


def main():
    if platform.system() == "Linux":
        serve()
    else:
        static()


if __name__ == "__main__":
    main()
