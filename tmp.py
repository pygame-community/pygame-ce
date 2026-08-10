import sys
import pygame as pg
from pygame.sprite import Sprite, Group, pointcollide, pointcollide_mask


# Create some sprite with a hole cut out of it to demonstrate mask usage.
class MySprite(Sprite):
    def __init__(self, rect: pg.Rect, *groups) -> None:
        super().__init__(*groups)

        self.image = pg.Surface([rect[2], rect[3]], flags=pg.SRCALPHA)
        self.image.fill("blue")

        center = (rect[2] // 2, rect[3] // 2)
        radius = (min(rect[2], rect[3]) - 2) / 2
        pg.draw.circle(self.image, (0, 0, 0, 0), center, radius)

        self.rect = rect


class Main:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((400, 300))
        self.clock = pg.time.Clock()
        self.group = Group()

        # make some sprite instances
        MySprite(pg.Rect(20, 20, 60, 60), self.group)
        MySprite(pg.Rect(60, 30, 40, 60), self.group)
        MySprite(pg.Rect(120, 120, 80, 80), self.group)

        self.indicator = pg.Surface([10, 10])
        self.indicator.fill("red")

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            mouse_pos = pg.mouse.get_pos()

            # uncomment either of these to alternate between collision using full rect, or masks.
            collisions = pointcollide(mouse_pos, self.group, False)
            # collisions=pointcollide(mouse_pos,self.group,False,pointcollide_mask)

            if collisions:
                self.indicator.fill("green")
            else:
                self.indicator.fill("red")
            print(collisions)

            self.screen.fill((200, 200, 200))
            self.group.draw(self.screen)
            self.screen.blit(self.indicator, (0, 290))
            pg.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    Main().run()
