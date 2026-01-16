import pygame

__tags__ = ["sdl3_skip"]

exclude = pygame.get_sdl_version() >= (3, 0, 0)

if exclude:
    __tags__.extend(("ignore", "subprocess_ignore"))
