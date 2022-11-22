import math
import random
from typing import List, Tuple

import pygame

from pyhb.typing_tester.generic_types import ColorValue, Events
from pyhb.utils import user_path


class TextManager:
    def __init__(
            self,
            screen: pygame.Surface,
            punctuation: bool,
            color: ColorValue,
            duration: int,
    ):
        self.font = pygame.font.SysFont("arialrounded", 24)
        self.color = color
        self.font_color = [255, 255, 255]
        self.font_error_color = [255, 0, 0]
        self.screen = screen
        self.screen_rect = screen.get_rect()
        with open(user_path + "/typing_tester/words.txt") as f:
            self.words = f.read()

        # User input
        self.user_passage: List[str] = [""]
        self.current_line = 0
        self.current_indices = {self.current_line: -1}
        self.cursor = "|"
        self.wpm, self.accuracy = 0, 0

        # Flags
        self.delete = True
        self.start_stack = False
        self.punctuation = punctuation
        self.correct = True
        self.start_test = False
        self.show_results = False
        self.calc_once = True

        # Count variables
        self.duration = duration
        self.time_left = duration
        self.time_passed = 0
        self.dt = 0
        self.cursor_count = 0
        self.delete_count = 0
        self.stack = 0
        self.characters_typed = 0
        self.correct_characters_typed = 0

        # Constant config variables
        self.FONT_WIDTH, self.FONT_HEIGHT = 13, 25
        self.DURATION = duration
        self.FORBIDDEN_CHARACTERS = (
            pygame.K_BACKSPACE,
            pygame.K_RETURN,
            pygame.KMOD_SHIFT,
        )
        self.MAX_LINE_LENGTH = 40
        self.CURSOR_COOLDOWN = 50
        self.DELETE_COOLDOWN = 6
        self.STACK_LIMIT = 60
        self.START_SCROLL_AFTER = 2

        # Surface
        self.surf = pygame.Surface(
            (self.screen.get_width(), 4 * self.font.get_height())
        )
        self.surf_rect = self.surf.get_rect()
        self.surf.set_colorkey((0, 0, 0))
        self.wpm_surf = self.font.render(str(self.wpm), True, self.font_color)
        self.accuracy_surf = self.font.render(str(self.accuracy), True, self.font_color)
        self.wpm_surf_rect = self.wpm_surf.get_rect()
        self.accuracy_surf_rect = self.accuracy_surf.get_rect()
        self.results_surf = pygame.Surface((200, self.font.get_height() * 2))
        self.results_surf_rect = self.results_surf.get_rect()
        self.results_surf.set_colorkey((0, 0, 0))

        # Time display
        self.time_txt = self.font.render(str(self.time_left), True, self.font_color)
        self.time_txt_rect = self.time_txt.get_rect()
        self.time_txt_pos = list((self.screen_rect.center[0], self.screen_rect.center[1] - 200))

        # Create passage & End __init__
        self.passage: List[str] = []
        self.append_passage(6)
        # -- END --

    def generate_valid_lines(self, n: int) -> List[str]:
        """
        :param n: Number of full sentences to be generated. Number of lines may differ.
        """

        lines = ""
        prev_word = " "
        for _ in range(n):
            line = ""
            while True:
                if self.punctuation:
                    word = random.choice(self.words.split())
                    if "." in prev_word:
                        word = word[0].upper() + word[1:]
                    elif prev_word[0].isupper():
                        pass
                    elif len(lines.split()) > 5:
                        word += "."
                else:
                    word = random.choice(self.words.split())
                prev_word = word
                line += word + " "
                if len(line) >= self.MAX_LINE_LENGTH:
                    line += "\n"
                    break
            lines += line

        return lines.split("\n")

    def calculate_results(self) -> Tuple[int, float]:
        """

        :return: WPM, Accuracy
        """
        num_correct_words = 0
        for word, correct_word in zip(
                " ".join(self.user_passage).split(), " ".join(self.user_passage).split()
        ):
            if word == correct_word:
                num_correct_words += 1

        wpm = int(num_correct_words * (60 / self.DURATION))
        accuracy = int((self.correct_characters_typed / self.characters_typed) * 100)

        return wpm, accuracy

    def append_passage(self, n: int) -> None:
        self.passage += self.generate_valid_lines(n)

    def move_pos(self, target_x: int, target_y: int, x: int, y: int, speed: float):
        # Getting the angle in radians
        angle = math.atan2(target_y - y, target_x - x)

        # Finding by how much to update position x and y to reach target
        ix = math.cos(angle) * speed * self.dt
        iy = math.sin(angle) * speed * self.dt

        return ix, iy

    def update(self, events: Events, dt: float, resize_frame: bool) -> None:
        """
        :param events: -> pygame.event.get()
        :param dt: Amount of time taken to complete last frame * FPS
        :param resize_frame: Has screen been resized this frame
        :return: None

        Updates the TextManager object
        """
        self.dt = dt

        # Handle screen resizing
        if resize_frame:
            self.screen_rect = self.screen.get_rect()
            self.time_txt_pos = list((self.screen_rect.center[0],
                                      self.screen_rect.center[1] - 200))

        # Handle timer
        self.time_txt = self.font.render(
            str(self.time_left), True, self.font_color
        )
        if self.start_test:
            self.time_passed += dt / 100
            if self.time_passed >= 1:
                self.time_left -= 1
                self.time_passed = 0
            if self.time_txt_pos[0] < self.screen_rect.topright[0] - self.time_txt_rect.width - 10:
                pad = 10
                target_x = self.screen_rect.topright[0] - self.time_txt_rect.width - pad
                target_y = self.screen_rect.topright[1] + pad
                increment_val = self.move_pos(target_x, target_y,
                                              self.time_txt_pos[0], self.time_txt_pos[1], speed=5)
                self.time_txt_pos[0] += increment_val[0]
                self.time_txt_pos[1] += increment_val[1]

        # Some update
        if self.time_left == 0:
            self.show_results = True
            self.start_test = False

        # Handle count variables
        self.cursor_count += self.dt
        if self.cursor_count >= self.CURSOR_COOLDOWN:
            self.cursor = "" if self.cursor else "|"
            self.cursor_count = 0

        self.delete_count += self.dt
        if self.delete_count >= self.DELETE_COOLDOWN:
            self.delete = True
            self.delete_count = 0

        if self.current_line >= len(self.passage) - 4:
            self.append_passage(3)
            self.passage.remove("")

        # Handle keyboard inputs
        # Event loop: single click
        for event in events:
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key not in self.FORBIDDEN_CHARACTERS:
                    self.cursor = "|"

                    self.current_indices[self.current_line] += 1
                    try:
                        if len(self.user_passage[self.current_line]) < len(
                                self.passage[self.current_line]
                        ):
                            self.user_passage[self.current_line] += event.unicode
                            self.start_test = True

                            # Update Accuracy variables
                            self.characters_typed += 1
                            if (
                                    event.unicode
                                    == self.passage[self.current_line][self.current_indices[self.current_line]]
                            ):
                                self.correct_characters_typed += 1
                        else:
                            print("DEBUG")
                    except ValueError:
                        pass

                    if self.current_line < len(self.passage) and len(
                            self.user_passage[self.current_line]
                    ) >= len(self.passage[self.current_line]):
                        self.current_line += 1
                        self.current_indices[self.current_line] = -1

                        self.user_passage.append("")
                elif event.key == pygame.K_BACKSPACE:
                    self.user_passage[self.current_line] = self.user_passage[
                                                               self.current_line
                                                           ][:-1]
                    self.current_indices[self.current_line] -= 1

                    if (
                            self.current_line != 0
                            and not self.user_passage[self.current_line]
                    ):
                        self.current_line -= 1

                    self.start_stack = True

        # keys: hold keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE] and self.delete and not self.start_stack:
            if self.user_passage[self.current_line]:
                self.user_passage[self.current_line] = self.user_passage[
                                                           self.current_line
                                                       ][:-1]
                self.current_indices[self.current_line] -= 1
                self.cursor = "|"
            elif self.current_line != 0:
                self.current_line -= 1
        elif self.start_stack:
            self.stack += self.dt
            if self.stack >= self.STACK_LIMIT:
                self.start_stack = False
                self.stack = 0

        self.delete = False

    def draw_text(self) -> None:
        """
        Draws the text

        :return: None
        """
        positions = []

        # Timer
        self.screen.blit(self.time_txt, tuple(self.time_txt_pos))

        # Shadow text
        for row, line in enumerate(self.passage):
            stub = []
            for column, char in enumerate(line):
                if (
                        self.current_line >= row
                        and self.current_indices[row] >= column
                        and self.user_passage[row]
                ):
                    try:
                        if self.user_passage[row][column] == self.passage[row][column]:
                            color = self.font_color
                        else:
                            color = self.font_error_color
                    except IndexError:
                        pass
                else:
                    color = self.font_color

                text = self.font.render(char, True, color)
                text.set_alpha(150)

                if self.current_line >= self.START_SCROLL_AFTER:
                    increment = (self.FONT_HEIGHT * -(self.current_line - self.START_SCROLL_AFTER))
                else:
                    increment = 0

                text_rect = text.get_rect(
                    center=(self.screen.get_rect().centerx - 250, 10 + increment)
                )
                # pos = (text_rect.topleft[0] + column * self.FONT_WIDTH, text_rect.topleft[1] + row * self.FONT_HEIGHT)
                pos = (
                    text_rect.topleft[0] + column * self.FONT_WIDTH,
                    (text_rect.topleft[1] + row * self.FONT_HEIGHT) +
                    ((self.screen.get_height() // 2) - (self.FONT_HEIGHT * self.START_SCROLL_AFTER))
                )

                stub.append(pos)
                self.screen.blit(text, pos)
            positions.append(stub)

        current_pos = list(self.current_indices.items())[-1]
        for row, line in enumerate(self.user_passage):
            for column, char in enumerate(line):
                curt = False
                if (row, column) == current_pos:
                    text = self.font.render(char + self.cursor, True, self.font_color)
                    curt = True
                else:
                    text = self.font.render(char, True, self.font_color)

                try:
                    if self.user_passage[row][column] == self.passage[row][column]:
                        self.screen.blit(text, positions[row][column])
                    elif curt:
                        cursor = self.font.render(self.cursor, True, self.font_color)
                        pos = (
                            positions[row][column][0] + self.FONT_WIDTH,
                            positions[row][column][1],
                        )
                        self.screen.blit(cursor, pos)
                except IndexError:
                    pass

        # self.surf_rect = self.surf.get_rect(center=screen_center)
        # self.screen.blit(self.surf, self.surf_rect)

    # TODO: Draw the results in a polished manner
    # Make an increasing number animation and completing arc animation
    def get_results(self, resize_frame: bool, color: ColorValue) -> None:
        """
        Draws the results at the end of the type test
        WPM and Accuracy

        :return: None
        """
        self.results_surf.fill((0, 0, 0))
        if resize_frame:
            self.screen_rect = self.screen.get_rect()

        self.wpm_surf = self.font.render(
            "wpm: " + str(self.wpm), True, self.font_color
        )
        self.accuracy_surf = self.font.render(
            "acc: " + str(self.accuracy) + "%", True, self.font_color
        )

        if self.calc_once:
            self.wpm, self.accuracy = self.calculate_results()
            self.wpm_surf_rect = self.wpm_surf.get_rect()
            self.accuracy_surf_rect = self.accuracy_surf.get_rect()
            self.calc_once = False

        self.results_surf_rect.topright = (self.screen_rect.topright[0] - 10,
                                           self.screen_rect.topright[1] + 10)
        self.wpm_surf_rect.midtop = self.results_surf_rect.midtop
        self.accuracy_surf_rect.midtop = (self.results_surf_rect.midtop[0],
                                          self.results_surf_rect.midtop[1] + self.font.get_height())

        self.screen.blit(self.wpm_surf, self.wpm_surf_rect)
        self.screen.blit(self.accuracy_surf, self.accuracy_surf_rect)
        pygame.draw.rect(self.screen, color, self.results_surf_rect, width=2)

    def draw(self) -> None:
        """
        Handles what to draw

        :return: None
        """
        self.surf.fill((0, 0, 0))

        if not self.show_results:
            self.draw_text()
