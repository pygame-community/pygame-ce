import pygame as pg
pg.init()
running = True
display = pg.display.set_mode((600, 600))
clock = pg.time.Clock()
n = 50
delta = -1

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

    display.fill("black")

    pg.draw.rect(display, (255, 255, 255), (100, 100, 50, 50), 4, n, n, n, -n, n)
    pg.draw.rect(display, (255, 255, 255), (100, 400, 50, 50), 100, n, n, n, -n, n)
    pg.draw.rect(display, (255, 255, 255), (400, 400, 50, 100), 0, n, n, n, -n, n)

    n += delta

    pg.display.update()

    if n == -100:
        delta = 1
    elif n == 10:
        delta = -1

    clock.tick(10)