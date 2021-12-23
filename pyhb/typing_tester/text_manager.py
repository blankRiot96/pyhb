import pygame
import random
from typing import List, Tuple
from pyhb.typing_tester.display import FPS
from pyhb.typing_tester.passage_generator import get_sentences, get_words
from pyhb.typing_tester.words import words


class TextManager:
    def __init__(
        self,
        screen: pygame.Surface,
        punctuation: bool,
        color: Tuple[int, int, int],
        duration: int,
    ):
        self.font = pygame.font.SysFont("leelawadee", 24)
        self.color = color
        self.font_color = [255, 255, 255]
        self.font_error_color = [255, 0, 0]
        self.screen = screen

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
        self.time_txt = self.font.render(str(self.time_left), True, self.font_color)
        self.wpm_surf = self.font.render(str(self.wpm), True, self.font_color)
        self.accuracy_surf = self.font.render(str(self.accuracy), True, self.font_color)
        self.results_surf = pygame.Surface((200, 200))
        self.results_surf.set_colorkey((0, 0, 0))

        # Create passage & End __init__
        self.passage: List[str] = []
        self.append_passage(6)
        # -- END --

    def generate_valid_lines(self, n: int = None, clington=None) -> List[str]:
        """
        :param n: Number of full sentences to be generated. Number of lines may differ.
        """

        lines = ""
        if self.punctuation or clington:
            if clington:
                punctuated_lines = clington
            else:
                punctuated_lines: List[str] = get_sentences(n)
            for p in punctuated_lines:
                line = ""
                for word in p.split():
                    line += word + " "
                    if len(line) >= self.MAX_LINE_LENGTH:
                        line += "\n"
                        break
                lines += line
        else:
            for _ in range(n):
                line = ""
                while True:
                    word = random.choice(words.split())
                    line += word + " "
                    if len(line) >= self.MAX_LINE_LENGTH:
                        line += "\n"
                        break
                lines += line

        return lines.split("\n")

    def calculate_results(self) -> (int, float):
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
        accuracy = round(
            (self.correct_characters_typed / self.characters_typed) * 100, 2
        )

        return wpm, accuracy

    def append_passage(self, n) -> None:
        self.passage += self.generate_valid_lines(n)

    def update(self, events, dt) -> None:
        """
        :param events: -> pygame.event.get()
        :param dt: Amount of time taken to complete last frame * FPS
        :return: None

        Updates the TextManager object
        """
        self.dt = dt

        # Handle timer
        if self.start_test:
            self.time_passed += dt / FPS
            if self.time_passed >= 1:
                self.time_left -= 1
                self.time_passed = 0
                self.time_txt = self.font.render(
                    str(self.time_left), True, self.font_color
                )

        if self.time_left == 0:
            self.show_results = True
            self.start_test = False

        # Handle count variables
        self.cursor_count += self.dt
        if self.cursor_count >= self.CURSOR_COOLDOWN:
            self.cursor = "|" if self.cursor else ""
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
                                == self.passage[self.current_line][
                                    self.current_indices[self.current_line]
                                ]
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

        :return: None

        Draws the text
        """
        screen_center = self.screen.get_rect().center
        positions = []

        # Timer
        # self.time_txt_rect = self.time_txt.get_rect(center=(screen_center[0], screen_center[0] - 100))
        self.screen.blit(self.time_txt, (screen_center[0], screen_center[1] - 200))

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
                    except IndexError as err:
                        print(err)
                        print(185)
                        print(row, column)
                        print(len(self.user_passage[self.current_line]))
                        print(len(self.passage[self.current_line]))

                        with open("debug_output/dump.txt", "w") as f:
                            f.write("\n".join(self.user_passage))

                        with open("debug_output/dump2.txt", "w") as f:
                            f.write("\n".join(self.passage))
                        exit()
                else:
                    color = self.font_color

                text = self.font.render(char, True, color)
                text.set_alpha(150)

                increment = (
                    (self.FONT_HEIGHT * -(self.current_line - self.START_SCROLL_AFTER))
                    if self.current_line >= self.START_SCROLL_AFTER
                    else 0
                )
                text_rect = text.get_rect(
                    center=(self.surf.get_rect().centerx - 250, 10 + increment)
                )
                # pos = (text_rect.topleft[0] + column * self.FONT_WIDTH, text_rect.topleft[1] + row * self.FONT_HEIGHT)

                pos = (
                    text_rect.topleft[0] + column * self.FONT_WIDTH,
                    text_rect.topleft[1] + row * self.FONT_HEIGHT,
                )

                stub.append(pos)
                # print(pos)
                self.surf.blit(text, pos)
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
                        self.surf.blit(text, positions[row][column])
                    elif curt:
                        cursor = self.font.render(self.cursor, True, self.font_color)
                        pos = (
                            positions[row][column][0] + self.FONT_WIDTH,
                            positions[row][column][1],
                        )
                        self.surf.blit(cursor, pos)
                except IndexError:
                    print(211)
                    print(row, column)
                    print(len(self.user_passage[self.current_line]))
                    print(len(self.passage[self.current_line]))

                    with open("dump.txt", "w") as f:
                        f.write("\n".join(self.user_passage))

                    with open("dump2.txt", "w") as f:
                        f.write("\n".join(self.passage))
                    exit()

        self.surf_rect = self.surf.get_rect(center=screen_center)
        self.screen.blit(self.surf, self.surf_rect)

    # TODO: Draw the results in a polished manner
    # Make an increasing number animation and completing arc animation
    def get_results(self) -> None:
        """

        :return: None

        Draws the results at the end of the type test
        Mainly WPM and Accuracy
        """
        self.results_surf.fill((0, 0, 0))
        screen_center = self.screen.get_rect().center

        # TODO: Crop self.results_surf accordingly with `pygame.transform.crop`
        if self.calc_once:
            self.wpm, self.accuracy = self.calculate_results()
            self.wpm_surf = self.font.render(
                "WPM: " + str(self.wpm), True, self.font_color
            )
            self.accuracy_surf = self.font.render(
                "Accuracy: " + str(self.accuracy) + "%", True, self.font_color
            )

            self.calc_once = False

        self.results_surf.blit(self.wpm_surf, (0, 0))
        self.results_surf.blit(self.accuracy_surf, (0, self.font.get_height()))

        # results_surf_rect = self.results_surf.get_bounding_rect()
        # results_surf_rect.center = screen_center
        #
        # self.screen.blit(self.results_surf, results_surf_rect)

    def draw(self) -> None:
        """

        :return: None

        Handles what to draw
        """
        self.surf.fill((0, 0, 0))

        if self.show_results:
            self.get_results()
        else:
            self.draw_text()
