import math
import pygame


def new_canvas():
    # Return a new blank canvas.
    return pygame.Surface((320, 240))


def main():
    pygame.init()
    clock = pygame.Clock()

    # Screen is a resizable window.
    screen = pygame.display.set_mode((320, 240), pygame.RESIZABLE)

    # Canvas is the surface to draw to.
    canvas = new_canvas()

    pygame.display.set_caption("Pygame - Retro scaling")

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # A fresh canvas to work on.
        canvas = new_canvas()

        # Fill the screen-surface with a background-color.
        screen.fill((128, 0, 0))

        # Fill the canvas-surface with a background-color.
        canvas.fill((0, 128, 0))

        # Render a circle to demonstrate the scaling.
        pygame.draw.circle(canvas, (255, 255, 255), (160, 120), 32)

        # Calculate the scale-factor for the canvas-surface.
        scale_width = math.floor(screen.get_width() / canvas.get_width())
        scale_height = math.floor(screen.get_height() / canvas.get_height())

        # Set scale to the smallest of width and height.
        scale = min(scale_width, scale_height)

        # Set scale to a minimum of 1.
        scale = max(scale, 1)

        # Scale the canvas-surface.
        canvas = pygame.transform.scale_by(canvas, scale)

        # Calculate the center for the screen-surface.
        screen_center_x = math.floor(screen.get_width() / 2)
        screen_center_y = math.floor(screen.get_height() / 2)

        # Calculate the center for the canvas-surface.
        canvas_center_x = math.floor(canvas.get_width() / 2)
        canvas_center_y = math.floor(canvas.get_height() / 2)

        # Calculate the new canvas-position.
        canvas_x = screen_center_x - canvas_center_x
        canvas_y = screen_center_y - canvas_center_y

        # Render the canvas-surface in the center of screen-surface.
        screen.blit(canvas, (canvas_x, canvas_y))

        pygame.display.flip()

        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
