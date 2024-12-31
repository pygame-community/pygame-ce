#!/usr/bin/env python
"""pygame.examples.ninepatch
Demonstrate the purpose of the 9-patch scale method and a way to implement it.

9-patch scaling allows us to scale a surface while keeping 4 corners intact.
This is very useful for GUI applications.

How it works:
The 4 corners are extracted from the original surface and pasted on the new surface.
The 4 sides in between the corners are scaled horizontally or vertically to fit
between the new surface corners.
The central part of the image is scaled and pasted.

In this example a green fill is used which can be done faster and easier with pygame.draw.rect
but usually you'd have a custom surface that needs intact corners.
"""

import os
import pygame

SCREEN_SIZE = pygame.Vector2(600, 500)
SCALE_SIZE = pygame.Vector2(500, 150)
INNER_SCALE_SIZE = pygame.Vector2(400, 115)
CORNER_SIZE = 20
INNER_CORNER_SIZE = 7


def ninepatch_scale(
    surface: pygame.Surface,
    size: pygame.typing.Point,
    corner_size: int,
    alpha: bool = True,
    smooth: bool = False,
    dest_surface: pygame.Surface | None = None,
) -> pygame.Surface:
    # the code of this function also emulates how a transform-like ninepatch function would likely behave
    if dest_surface is not None:
        ret_surface = dest_surface
        if ret_surface.size != size:
            raise ValueError("Destination surface doesn't match the provided size")
    else:
        ret_surface = pygame.Surface(
            size, pygame.SRCALPHA * alpha
        )  # when alpha is False the flags become 0

    # aliases
    ret_w, ret_h = size  # non-sequence argument caught by python
    src_w, src_h = surface.size
    c = corner_size
    scale_func = pygame.transform.smoothscale if smooth else pygame.transform.scale
    subsurface = surface.subsurface  # alias for performance/clarity

    if corner_size < 0 or corner_size > min(ret_w, ret_h):
        raise ValueError(
            "Corner size must be nonnegative and not greater than the smaller between width and height"
        )
    if corner_size == 0:  # default to normal scaling
        return scale_func(surface, size)

    src_x_side, src_y_side = surface.size - pygame.Vector2(c) * 2
    ret_x_side, ret_y_side = size - pygame.Vector2(c) * 2

    ret_surface.blit(  # topleft corner
        subsurface(0, 0, c, c), (0, 0)
    )
    ret_surface.blit(  # topright corner
        subsurface(src_w - c, 0, c, c), (ret_w - c, 0)
    )
    ret_surface.blit(  # bottomleft corner
        subsurface(0, src_h - c, c, c), (0, ret_h - c)
    )
    ret_surface.blit(  # bottomright corner
        subsurface(src_w - c, src_h - c, c, c), (ret_w - c, ret_h - c)
    )

    if src_x_side > 0:
        ret_surface.blit(  # top side
            scale_func(subsurface(c, 0, src_x_side, c), (ret_x_side, c)), (c, 0)
        )
        ret_surface.blit(  # bottom side
            scale_func(subsurface(c, src_h - c, src_x_side, c), (ret_x_side, c)),
            (c, ret_h - c),
        )

    if src_y_side > 0:
        ret_surface.blit(  # left side
            scale_func(subsurface(0, c, c, src_y_side), (c, ret_y_side)), (0, c)
        )
        ret_surface.blit(  # right side
            scale_func(subsurface(src_w - c, c, c, src_y_side), (c, ret_y_side)),
            (ret_w - c, c),
        )

    if src_x_side > 0 and src_y_side > 0:
        ret_surface.blit(  # central area
            scale_func(
                subsurface(c, c, src_x_side, src_y_side), (ret_x_side, ret_y_side)
            ),
            (c, c),
        )

    return ret_surface


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("9-Patch Scale and Normal Scale Example")
    clock = pygame.Clock()
    font = pygame.Font(None, 30)

    main_dir = os.path.split(os.path.abspath(__file__))[0]
    example_image = pygame.image.load(os.path.join(main_dir, "data", "frame.png"))

    original_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.rect(
        original_surface, "green", original_surface.get_rect(), 0, CORNER_SIZE
    )

    normal_scale = pygame.transform.scale(original_surface, SCALE_SIZE)
    normal_center = SCREEN_SIZE.elementwise() / pygame.Vector2(2, 4)
    normal_rect = normal_scale.get_rect(center=normal_center)
    example_normal_scale = pygame.transform.scale(example_image, INNER_SCALE_SIZE)
    example_normal_rect = example_normal_scale.get_rect(center=normal_center)

    ninepatch = ninepatch_scale(
        original_surface, SCALE_SIZE, CORNER_SIZE, True, False, None
    )
    ninepatch_center = SCREEN_SIZE.elementwise() / pygame.Vector2(2, 4 / 3)
    ninepatch_rect = ninepatch.get_rect(center=ninepatch_center)
    example_ninepatch = ninepatch_scale(
        example_image, INNER_SCALE_SIZE, INNER_CORNER_SIZE, True, False, None
    )
    example_ninepatch_rect = example_ninepatch.get_rect(center=ninepatch_center)

    text_normal = font.render("Normal Scale", True, "black")
    text_normal_rect = text_normal.get_rect(center=normal_center)
    text_9patch = font.render("9-Patch Scale", True, "black")
    text_9patch_rect = text_9patch.get_rect(center=ninepatch_center)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(0)

        screen.blit(normal_scale, normal_rect)
        screen.blit(example_normal_scale, example_normal_rect)
        screen.blit(ninepatch, ninepatch_rect)
        screen.blit(example_ninepatch, example_ninepatch_rect)
        screen.blit(text_normal, text_normal_rect)
        screen.blit(text_9patch, text_9patch_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
