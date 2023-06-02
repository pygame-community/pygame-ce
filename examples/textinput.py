import pygame
from pygame.locals import *
import os
import time

"""
A little "console" where you can write in text.
Shows how to use the TEXTEDITING and TEXTINPUT events.
"""


os.environ["SDL_IME_SHOW_UI"] = "1"

pygame.init()


class Game:
    def __init__(self):
        """Define the game's variables."""
        self.screen = pygame.display.set_mode((700, 500))
        pygame.display.set_caption("Text Input")
        self.pos = []
        self.text = ""
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 700, 500
        self.chat_list = []

        self.holding_shift = False

    def get_fonts(self):
        """Gets the fonts"""
        self.font_names = [
            "notosanscjktcregular",
            "notosansmonocjktcregular",
            "notosansregular",
            "microsoftjhenghei",
            "microsoftyahei",
            "msgothic",
            "msmincho",
            "unifont",
            "Arial",
        ]

        self.FONT_NAMES = ",".join(str(x) for x in self.font_names)
        self.font = pygame.font.SysFont(self.font_names, 32)
        self.small_font = pygame.font.SysFont(self.font_names, 32)
        print("Using font: " + self.font.name)

    def handle_events(self, y_pos):
        # Handles the events
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_LSHIFT:
                    self.holding_shift = False
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if self.text != "":
                        self.chat_list.append(self.text)
                    self.text = ""

                if event.key == K_SPACE:
                    self.text += " "

                if event.key == K_LSHIFT:
                    self.holding_shift = True

                if event.key == K_BACKSPACE:
                    new_text_list = list(self.text)
                    new_text = ""

                    for i, char in enumerate(new_text_list):
                        if i == len(new_text_list) - 1:
                            new_text_list.pop(i)

                    for c in new_text_list:
                        new_text += c

                    self.text = new_text
            if event.type == TEXTINPUT:
                last_line_pos = 0
                for i, chr in enumerate(self.text):
                    if chr == "\n":
                        last_line_pos = i

                if y_pos < self.SCREEN_HEIGHT - 100:
                    self.text += event.text
                if len(self.text) - last_line_pos < 35:
                    pass
                else:
                    self.text += "\n"

            if event.type == QUIT:
                pygame.quit()
                exit()

    def update(self):
        """Renders all of the text and all of the chat messages."""
        message_spacing = 50
        self.get_fonts()
        while True:
            self.input_img = self.font.render(
                ">" + self.text + ["|", ""][int(time.time() % 2)], True, (25, 255, 100)
            )

            y_pos = self.input_img.get_height() + message_spacing
            self.screen.fill((0, 0, 0))

            msg_imgs = []

            for msg in self.chat_list:
                msg_imgs.append(self.small_font.render(msg, True, (25, 255, 100)))

            # checks if the y position is bigger than 500, if its bigger than 500, it will remove the first three items of the chat list.

            self.handle_events(y_pos)  # checks for the events
            for msg_img in msg_imgs:
                self.screen.blit(msg_img, (0, y_pos))
                y_pos += msg_img.get_height()

            if y_pos > self.SCREEN_HEIGHT:
                for i in range(3):
                    if len(self.chat_list) > 0:
                        self.chat_list.pop(i)
            self.screen.blit(self.input_img, (0, 0))
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.update()
