import pygame
import random
from typing import List, Tuple, Union
from pyhb.typing_tester.passage_generator import get_sentences, get_words
from pyhb.typing_tester.words import words


class TextManager:
    def __init__(self, screen: pygame.Surface, punctuation: bool, color: Tuple[int, int, int]):
        self.font = pygame.font.SysFont("leelawadee", 25)
        self.color = color
        self.screen = screen

        # User input
        self.user_passage: List[str] = [""]
        self.current_line = 0
        self.cursor = "|"

        # Flags 
        self.delete = True
        self.start_stack = False
        self.punctuation = punctuation

        # Count variables
        self.dt = 0
        self.cursor_count = 0
        self.delete_count = 0
        self.stack = 0

        # Constant config variables
        self.MAX_LINE_LENGTH = 50 
        self.CURSOR_COOLDOWN = 50
        self.DELETE_COOLDOWN = 6
        self.STACK_LIMIT = 60

        self.passage: List[str] = []
        self.append_passage(6)

        

    def generate_valid_lines(self, n: int) -> List[str]:
        """
        :param n: Number of full sentences to be generated. Number of lines may differ.
        """

        lines = ""
        if self.punctuation:
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


    def append_passage(self, n) -> None:
        self.passage += self.generate_valid_lines(n)


    def update(self, dt) -> None:
        self.dt = dt

        # Handle count variables
        self.cursor_count += self.dt
        if self.cursor_count >= self.CURSOR_COOLDOWN:
            self.cursor = "|" if self.cursor == "" else ""
            self.cursor_count = 0

        self.delete_count += self.dt
        if self.delete_count >= self.DELETE_COOLDOWN:
            self.delete = True
            self.delete_count = 0

        # Handle keyboard inputs
        
        # Event loop: single click
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if not event.key == pygame.K_BACKSPACE:
                    try:
                        self.user_passage[self.current_line] += event.unicode
                    except ValueError:
                        pass

                    if len(self.user_passage[self.current_line]) >= len(self.passage[self.current_line]):
                        self.current_line += 1
                        self.user_passage.append("")
                else:
                    self.user_passage[self.current_line] = self.user_passage[self.current_line][:-1]
                    if self.current_line != 0 and not self.user_passage[self.current_line]:
                        self.current_line -= 1
                    self.start_stack = True

        # keys: hold keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE] and self.delete and not self.start_stack:
            if self.user_passage[self.current_line]:
                self.user_passage[self.current_line] = self.user_passage[self.current_line][:-1]
            elif self.current_line != 0:
                print("REDACTED")
                self.current_line -= 1
        elif self.start_stack:
            self.stack += self.dt
            if self.stack >= self.STACK_LIMIT:
                self.start_stack = False
                self.stack = 0


        self.delete = False


    def draw(self) -> None:
        positions = []

        # Shadow text
        for index, line in enumerate(self.passage):
            text = self.font.render(line, True, 'white')
            text.set_alpha(150)
            text_rect = text.get_rect(center=self.screen.get_rect().center)
            pos = (text_rect.topleft[0], text_rect.topleft[1] + index * text_rect.height)
        
            positions.append(pos)

            self.screen.blit(text, pos)
        
        # User text
        for index, line in enumerate(self.user_passage):
            if index == self.current_line:
                line += self.cursor
            
            compliment = len(self.passage[index]) - len(self.user_passage[index])
            buffer = " "*compliment
            line += buffer
            text = self.font.render(line, True, 'white')

            self.screen.blit(text, positions[index])
        


