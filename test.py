from pygame import _render

import pygame


pygame.init()
_render.set_line_render_method("test")