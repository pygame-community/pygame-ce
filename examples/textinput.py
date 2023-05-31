import pygame
from pygame.locals import *
import time

pygame.init()

class Game:
    def __init__(self):
        


        self.screen = pygame.display.set_mode((700, 500))
        pygame.display.set_caption("Text Input")
        self.pos = []
        self.text = ""
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 700, 500
        self.chat_list = []
        self.char_list = list('abcdefghijklmnopqrstuvwxyz0123456789-=[]"') + list(
            "';,./"
        )
        self.font = pygame.font.SysFont("Arial", 32) #Creates the normal font
        self.small_font = pygame.font.SysFont("Arial", 22) #Creates the small font
        self.holding_shift = False
    def handle_events(self):
        #Handles the events
        for event in pygame.event.get():
            
                if event.type == KEYUP: #Checks if a key is released
                    if event.key == K_LSHIFT: 
                        self.holding_shift = False
                if event.type == KEYDOWN: # Checks if a key is pressed
                    if event.key == K_RETURN:
                        self.chat_list.append(self.text)

                    if event.key == K_SPACE:#Checks if the space key is pressed
                        self.text += " " #Adds a blank space to the text

                    if event.key == K_LSHIFT:#Checks if the shift key is being hold
                        self.holding_shift = True
                    else:
                        if pygame.key.name(event.key) in self.char_list:
                            if not "\n" in self.text:
                                if not self.holding_shift: #Checks if the player is not holding shift
                                    self.text = self.text + pygame.key.name(event.key)
                                else:
                                    if pygame.key.name(event.key) not in list(
                                        "0123456789/.,"
                                    ):
                                        self.text = (
                                            self.text
                                            + pygame.key.name(event.key).upper()
                                        )
                                    elif pygame.key.name(event.key) == "1":
                                        self.text += "!"
                                    elif pygame.key.name(event.key) == "2":
                                        self.text += "@"
                                    elif pygame.key.name(event.key) == "3":
                                        self.text += "#"
                                    elif pygame.key.name(event.key) == "4":
                                        self.text += "$"
                                    elif pygame.key.name(event.key) == "5":
                                        self.text += "%"
                                    elif pygame.key.name(event.key) == "6":
                                        self.text += "^"
                                    elif pygame.key.name(event.key) == "7":
                                        self.text += "&"
                                    elif pygame.key.name(event.key) == "8":
                                        self.text += "*"
                                    elif pygame.key.name(event.key) == "9":
                                        self.text += "("
                                    elif pygame.key.name(event.key) == "0":
                                        self.text += ")"
                                    elif pygame.key.name(event.key) == "/":
                                        self.text += "?"
                                    elif pygame.key.name(event.key) == ".":
                                        self.text += ">"
                                    elif pygame.key.name(event.key) == ",":
                                        self.text += "<"
                                if len(self.text) < 30: #Checks if the text variable has more than 30 characters
                                    pass
                                else:
                                    self.text += "\n"
                            else:
                                for i, chr in enumerate(self.text):
                                    if chr == "\n":
                                        last_line_pos = i

                                if not self.holding_shift:
                                    self.text = self.text + pygame.key.name(event.key)
                                else:
                                    if pygame.key.name(event.key) not in list(
                                        "0123456789/.,"
                                    ):
                                        self.text = (
                                            self.text
                                            + pygame.key.name(event.key).upper()
                                        )
                                    elif pygame.key.name(event.key) == "1":
                                        self.text += "!"
                                    elif pygame.key.name(event.key) == "2":
                                        self.text += "@"
                                    elif pygame.key.name(event.key) == "3":
                                        self.text += "#"
                                    elif pygame.key.name(event.key) == "4":
                                        self.text += "$"
                                    elif pygame.key.name(event.key) == "5":
                                        self.text += "%"
                                    elif pygame.key.name(event.key) == "6":
                                        self.text += "^"
                                    elif pygame.key.name(event.key) == "7":
                                        self.text += "&"
                                    elif pygame.key.name(event.key) == "8":
                                        self.text += "*"
                                    elif pygame.key.name(event.key) == "9":
                                        self.text += "("
                                    elif pygame.key.name(event.key) == "0":
                                        self.text += ")"
                                    elif pygame.key.name(event.key) == "/":
                                        self.text += "?"
                                    elif pygame.key.name(event.key) == ".":
                                        self.text += ">"
                                    elif pygame.key.name(event.key) == ",":
                                        self.text += "<"

                                if len(self.text) - last_line_pos < 35: # Checks if the difference between
                                    pass
                                else:
                                    self.text += "\n"

                    if event.key == K_RETURN:
                        self.text = ""
                    if event.key == K_BACKSPACE:
                        new_text_list = list(self.text)
                        new_text = ""

                        for i, char in enumerate(new_text_list):
                            if i == len(new_text_list) - 1:
                                new_text_list.pop(i)

                        for c in new_text_list:
                            new_text += c

                        self.text = new_text

                if event.type == QUIT:
                    pygame.quit()
                    exit()
    def update(self):
        message_spacing = 40
        while True:
            self.screen.fill((0, 0, 0))
            self.input_img = self.font.render( #creates the font surface
                "> "  + self.text + ["|", ""][int(time.time() * 2 % 2)], #"> " Makes the small little arrow, ["|", ""][int(time.time() * 2 % 2)] makes the cursor that you see when typing text
                False,
                (25, 255, 100),
            )

            
            msg_imgs = []
            y_pos = self.input_img.get_height() + message_spacing
            for msg in self.chat_list:
                msg_imgs.append(self.small_font.render(msg, False, (25, 255, 100)))
            
            # checks if the y position is bigger than 500, if its bigger than 500, it will remove the first three items of the chat list.
            if y_pos > 500:
                for i in range(3):
                    self.chat_list.pop(i)
                y_pos = self.input_img.get_height() + 40

            # checks for the events
            self.handle_events()
            
            for msg_img in msg_imgs:
                self.screen.blit(msg_img, (self.SCREEN_WIDTH//2-msg_img.get_width()//2, y_pos))
                y_pos += msg_img.get_height()

            self.screen.blit(self.input_img, (0, 0))
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.update()
