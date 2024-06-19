import pygame
from pygame import *  # pylint: disable=wildcard-import; lgtm[py/polluting-import]

pygame.set_warnings_filter(2)

# TODO: Should we initialize here?
# pygame.print_debug_info() gives more information afterwards,
# but are there any side-effects of doing this?
pygame.init()

pygame.print_debug_info()
