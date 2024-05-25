#!/usr/bin/env python
"""pygame.examples.textinput

A little "console" where you can write in text.

Shows how to use the TEXTEDITING and TEXTINPUT events.
"""

from typing import Tuple, List
import sys
import os

import pygame

# This environment variable is important
# If not added the candidate list will not show
os.environ["SDL_IME_SHOW_UI"] = "1"


class TextInput:
    """
    A simple TextInput class that allows you to receive inputs in pygame.
    """

    # Add font name for each language,
    # otherwise some text can't be correctly displayed.
    FONT_NAMES = [
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

    def __init__(
        self,
        prompt: str,
        pos: Tuple[int, int],
        screen_dimensions: Tuple[int, int],
        print_event: bool,
        text_color="white",
        fps: int = 50,
    ) -> None:
        self.prompt = prompt
        self.print_event = print_event
        # position of chatlist and chatbox
        self.CHAT_LIST_POS = pygame.Rect(
            (pos[0], pos[1] + 50), (screen_dimensions[0], 400)
        )
        self.CHAT_BOX_POS = pygame.Rect(pos, (screen_dimensions[1], 40))
        self.CHAT_LIST_MAXSIZE = 20

        self._ime_editing = False
        self._ime_text = ""
        self._ime_text_pos = 0
        self._ime_editing_text = ""
        self._ime_editing_pos = 0
        self.chat = ""

        # The font name can be a comma separated list
        # of font names to search for.
        self.font_names = ",".join(self.FONT_NAMES)
        self.font = pygame.font.SysFont(self.font_names, 24)
        self.font_height = self.font.get_height()
        self.font_small = pygame.font.SysFont(self.font_names, 16)
        self.text_color = text_color

        self.prompt_surf = self.font.render(self.prompt, True, self.text_color)
        self.prompt_rect = self.prompt_surf.get_rect(topleft=self.CHAT_BOX_POS.topleft)

        self.fps = fps
        self.second_counter = 0

        print("Using font: " + self.font.name)

    def update(self, events: List[pygame.Event]) -> None:
        """
        Updates the text input widget
        """
        for event in events:
            self.handle_event(event)

        self.second_counter += 1

        if self.second_counter >= self.fps:
            self.second_counter = 0

        # Check if input fits in chat box
        input_size = self.font.size(self._get_ime_text())
        while input_size[0] > self.CHAT_BOX_POS.w - self.prompt_rect.w:
            if self._ime_editing_text:
                # Don't block.
                break
            self._ime_text = self._ime_text[:-1]
            input_size = self.font.size(self._get_ime_text())

    def _clamp_to_text_range(self, num: int):
        return min(len(self._ime_text), max(0, num))

    def move_cursor_by(self, by: int):
        self._ime_text_pos = self._clamp_to_text_range(self._ime_text_pos + by)

    def replace_chars(
        self,
        remove_count: int = 0,
        to_insert: str = "",
        text_after_cursor: bool = False,
    ):
        """
        Removes given number of characters from the cursor location
        and adds an optional string there, then adjusts the cursor location.
        """
        loc = self._clamp_to_text_range(remove_count + self._ime_text_pos)

        if remove_count < 0:
            self._ime_text = (
                self._ime_text[0:loc] + to_insert + self._ime_text[self._ime_text_pos :]
            )

            if text_after_cursor:
                self.move_cursor_by(remove_count)
            else:
                self.move_cursor_by(remove_count + len(to_insert))
        else:
            self._ime_text = (
                self._ime_text[0 : self._ime_text_pos]
                + to_insert
                + self._ime_text[loc:]
            )

            # Don't move cursor if not inserting text
            # after removing the characters in front of the cursor
            if not text_after_cursor:
                self.move_cursor_by(len(to_insert))

    def handle_event(self, event: pygame.Event):
        """
        Handle an event
        """
        if self.print_event:
            print(event)

        if event.type == pygame.KEYDOWN:
            if self._ime_editing:
                if len(self._ime_editing_text) == 0:
                    self._ime_editing = False
                return

            if event.key == pygame.K_BACKSPACE:
                self.replace_chars(-1)

            elif event.key == pygame.K_DELETE:
                self.replace_chars(1)

            elif event.key == pygame.K_LEFT:
                self.move_cursor_by(-1)

            elif event.key == pygame.K_RIGHT:
                self.move_cursor_by(1)

            # Handle ENTER key
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                # Block if we have no text to append
                if len(self._ime_text) == 0:
                    return

                # Add to chat log
                self.chat += self._ime_text + "\n"

                chat_lines = self.chat.split("\n")
                if len(chat_lines) > self.CHAT_LIST_MAXSIZE:
                    chat_lines.pop(0)
                    self.chat = "\n".join(chat_lines)

                self._ime_text = ""
                self._ime_text_pos = 0

        elif event.type == pygame.TEXTEDITING:
            self._ime_editing = True
            self._ime_editing_text = event.text
            self._ime_editing_pos = event.start

        elif event.type == pygame.TEXTINPUT:
            self._ime_editing = False
            self._ime_editing_text = ""
            self.replace_chars(to_insert=event.text)

    def _get_ime_text(self):
        """
        Returns text that is currently in input.
        """
        if self._ime_editing_text:
            return (
                f"{self._ime_text[0: self._ime_text_pos]}"
                f"[{self._ime_editing_text}]"
                f"{self._ime_text[self._ime_text_pos:]}"
            )
        return (
            f"{self._ime_text[0: self._ime_text_pos]}"
            f"{self._ime_text[self._ime_text_pos:]}"
        )

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the text input widget onto the provided surface
        """

        chat_list_surf = self.font_small.render(
            self.chat, True, self.text_color, wraplength=self.CHAT_LIST_POS.width
        )

        screen.blit(chat_list_surf, self.CHAT_LIST_POS)

        # Chat box updates
        cursor_loc = self._ime_text_pos + self._ime_editing_pos
        ime_text = self._get_ime_text()

        text_surf = self.font.render(
            ime_text, True, self.text_color, wraplength=self.CHAT_BOX_POS.width
        )

        text_rect = text_surf.get_rect(topleft=self.prompt_rect.topright)
        screen.blit(self.prompt_surf, self.prompt_rect)
        screen.blit(text_surf, text_rect)

        # Show blinking cursor, blink twice a second.
        if self.second_counter * 2 < self.fps:
            # Characters can have different widths,
            # so calculating the correct location for the cursor is required.
            metrics = self.font.metrics(ime_text)
            x_location = 0

            index = 0
            for metric in metrics:
                if metric is None:
                    continue

                _, _, _, _, x_advance = metric

                if index >= cursor_loc:
                    break
                x_location += x_advance
                index += 1

            cursor_rect = pygame.Rect(
                x_location + text_rect.x, text_rect.y, 2, self.font_height
            )
            pygame.draw.rect(screen, self.text_color, cursor_rect)


class Game:
    """
    A class that handles the game's events, mainloop etc.
    """

    # CONSTANTS
    # Frames per second, the general speed of the program
    FPS = 50
    # Size of window
    SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
    BG_COLOR = "black"

    def __init__(self, caption: str) -> None:
        # Initialize
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption(caption)
        self.clock = pygame.Clock()

        # Text input
        # Set to true or add 'showevent' in argv to see IME and KEYDOWN events
        self.print_event = "showevent" in sys.argv
        self.text_input = TextInput(
            prompt="> ",
            pos=(0, 20),
            screen_dimensions=(self.SCREEN_WIDTH, self.SCREEN_HEIGHT),
            print_event=self.print_event,
            text_color="green",
            fps=self.FPS,
        )

    def main_loop(self) -> None:
        pygame.key.start_text_input()
        input_rect = pygame.Rect(80, 80, 320, 40)
        pygame.key.set_text_input_rect(input_rect)

        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.text_input.update(events)

            # Screen updates
            self.screen.fill(self.BG_COLOR)
            self.text_input.draw(self.screen)

            pygame.display.update()
            self.clock.tick(self.FPS)


# Main loop process
def main():
    game = Game("Text Input Example")
    game.main_loop()


if __name__ == "__main__":
    main()
