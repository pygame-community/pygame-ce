from types import SimpleNamespace

import pygame


def update_regions(window) -> SimpleNamespace:
    regions = SimpleNamespace(
        drag=pygame.Rect((0, 0), window.size).inflate(-200, -200),
        top=pygame.Rect(window.size[0] / 2 - 200 / 2, 0, 200, 50),
        topleft=pygame.Rect(0, 0, 60, 60),
        left=pygame.Rect(0, window.size[1] / 2 - 120 / 2, 70, 120),
        bottomleft=pygame.Rect(0, window.size[1] - 60, 60, 60),
        bottom=pygame.Rect(window.size[0] / 2 - 200 / 2, window.size[1] - 50, 200, 50),
        bottomright=pygame.Rect(window.size[0] - 60, window.size[1] - 60, 60, 60),
        right=pygame.Rect(window.size[0] - 70, window.size[1] / 2 - 120 / 2, 70, 120),
        topright=pygame.Rect(window.size[0] - 60, 0, 60, 60),
    )

    window.clear_special_regions()
    window.add_drag_region(regions.drag)
    window.add_resize_region(regions.top, "top")
    window.add_resize_region(regions.topleft, "topleft")
    window.add_resize_region(regions.left, "left")
    window.add_resize_region(regions.bottomleft, "bottomleft")
    window.add_resize_region(regions.bottom, "bottom")
    window.add_resize_region(regions.bottomright, "bottomright")
    window.add_resize_region(regions.right, "right")
    window.add_resize_region(regions.topright, "topright")

    return regions


def draw(screen: pygame.Surface, font: pygame.Font, regions: SimpleNamespace) -> None:
    screen.fill((60, 60, 60))
    pygame.draw.rect(screen, "white", screen.get_rect().inflate(-30, -30), width=4)

    def draw_box(rect, text):
        pygame.draw.rect(screen, (100, 100, 100), rect)
        text_rect = rect.inflate(-20, -20)
        text_surf = font.render(text, True, "white", wraplength=max(1, text_rect.width))
        screen.blit(text_surf, text_rect.topleft)

    draw_box(regions.drag, "drag me to move the window\nPress Esc to exit")
    draw_box(regions.top, "drag me to resize")
    draw_box(regions.topleft, "drag me")
    draw_box(regions.left, "drag me to resize")
    draw_box(regions.bottomleft, "drag me")
    draw_box(regions.bottom, "drag me to resize")
    draw_box(regions.bottomright, "drag me")
    draw_box(regions.right, "drag me to resize")
    draw_box(regions.topright, "drag me")


def main():
    pygame.init()

    font = pygame.font.Font(size=24)

    window = pygame.Window(size=(640, 480), borderless=True, resizable=True)
    window.minimum_size = (480, 360)
    screen = window.get_surface()

    regions = update_regions(window)
    trigger_count = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.WINDOWREGIONTRIGGERED:
                trigger_count += 1
                print(f"special window region triggered (#{trigger_count})")

            if event.type == pygame.WINDOWRESIZED:
                regions = update_regions(window)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                raise SystemExit

        draw(screen, font, regions)
        window.flip()


if __name__ == "__main__":
    main()
