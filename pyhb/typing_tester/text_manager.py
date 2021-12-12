import pygame
import random
from typing import List, Tuple, Union
from pyhb.typing_tester.passage_generator import get_sentences, get_words
from pyhb.typing_tester.words import words


class TextManager:
    def __init__(self, screen: pygame.Surface, punctuation: bool, color: Tuple[int, int, int]):
        self.font = pygame.font.SysFont("leelawadee", 24)
        self.color = color
        self.screen = screen

        # User input
        self.user_passage: List[str] = [""]
        self.current_line = 0
        self.current_indeces = {
            self.current_line: -1
        }
        self.cursor = "|"

        # Flags 
        self.delete = True
        self.start_stack = False
        self.punctuation = punctuation
        self.correct = True

        # Count variables
        self.dt = 0
        self.cursor_count = 0
        self.delete_count = 0
        self.stack = 0

        # Constant config variables
        self.FONT_WIDTH, self.FONT_HEIGHT = 13, 25
        self.MAX_LINE_LENGTH = 40
        self.CURSOR_COOLDOWN = 50
        self.DELETE_COOLDOWN = 6
        self.STACK_LIMIT = 60
        self.START_SCROLL_AFTER = 2

        # Surface
        self.surf = pygame.Surface((self.screen.get_width(), 4 * self.font.get_height()))
        self.surf_rect = self.surf.get_rect()
        self.surf.set_colorkey((0, 0, 0))

        self.passage: List[str] = []
        self.append_passage(6)

        

    def generate_valid_lines(self, n: int=None, clington=None) -> List[str]:
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


    def append_passage(self, n) -> None:
        self.passage += self.generate_valid_lines(n)


    def update(self, events, dt) -> None:
        # self.passage = self.generate_valid_lines(clington=self.passage)
        self.dt = dt

        # index = len(self.user_passage[self.current_line])
        # if self.user_passage[self.current_line] == self.passage[self.current_line][:index]:
        #     self.correct = True
        # else:
        #     self.correct = False

        # Handle count variables
        self.cursor_count += self.dt
        if self.cursor_count >= self.CURSOR_COOLDOWN:
            self.cursor = "|" if self.cursor == "" else ""
            self.cursor_count = 0

        self.delete_count += self.dt
        if self.delete_count >= self.DELETE_COOLDOWN:
            self.delete = True
            self.delete_count = 0

        if self.current_line >= len(self.passage) - 4:
            self.append_passage(3)
            self.passage.remove('')

        # Handle keyboard inputs
        # Event loop: single click
        for event in events:
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key != pygame.K_BACKSPACE:
                    self.cursor = "|"

                    self.current_indeces[self.current_line] += 1
                    try:
                        if len(self.user_passage[self.current_line]) < len(self.passage[self.current_line]):
                            self.user_passage[self.current_line] += event.unicode
                        else:
                            print('DEBUG')
                    except ValueError:
                        pass

                    if self.current_line < len(self.passage) and len(self.user_passage[self.current_line]) >= len(self.passage[self.current_line]):
                        self.current_line += 1
                        self.current_indeces[self.current_line] = -1

                        self.user_passage.append("")
                else:
                    self.user_passage[self.current_line] = self.user_passage[self.current_line][:-1]                    
                    self.current_indeces[self.current_line] -= 1

                    if self.current_line != 0 and not self.user_passage[self.current_line]:
                        self.current_line -= 1


                    self.start_stack = True

        # keys: hold keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE] and self.delete and not self.start_stack:
            if self.user_passage[self.current_line]:
                self.user_passage[self.current_line] = self.user_passage[self.current_line][:-1]
                self.current_indeces[self.current_line] -= 1
                self.cursor = "|"
            elif self.current_line != 0:
                self.current_line -= 1
        elif self.start_stack:
            self.stack += self.dt
            if self.stack >= self.STACK_LIMIT:
                self.start_stack = False
                self.stack = 0


        self.delete = False


    def draw(self) -> None:
        self.surf.fill(0)
        screen_center = self.screen.get_rect().center
        screen_topleft = self.screen.get_rect().topleft
        positions = []


        # Shadow text
        for row, line in enumerate(self.passage):
            stub = []
            for column, char in enumerate(line):
                if self.current_line >= row and self.current_indeces[row] >= column and self.user_passage[row]:
                    try:
                        if self.user_passage[row][column] == self.passage[row][column]:
                            color = 'white'
                        else:
                            color = 'red'
                    except IndexError:
                        print(185)
                        print(row, column)

                        with open('dump.txt', 'w') as f:
                            f.write("\n".join(self.user_passage))
                        
                        with open('dump2.txt', 'w') as f:
                            f.write("\n".join(self.passage))
                        exit()
                else:
                    color = 'white'

                text = self.font.render(char, True, color)
                text.set_alpha(150)


                increment = (self.FONT_HEIGHT * -(self.current_line - self.START_SCROLL_AFTER)) if self.current_line >= self.START_SCROLL_AFTER else 0
                text_rect = text.get_rect(center=(self.surf.get_rect().centerx - 250, 10 + increment))
                # pos = (text_rect.topleft[0] + column * self.FONT_WIDTH, text_rect.topleft[1] + row * self.FONT_HEIGHT)

                pos = (text_rect.topleft[0] + column * self.FONT_WIDTH, text_rect.topleft[1] + row * self.FONT_HEIGHT)

                stub.append(pos)
                # print(pos)
                self.surf.blit(text, pos)
            positions.append(stub)

        current_pos = list(self.current_indeces.items())[-1]
        for row, line in enumerate(self.user_passage):
            for column, char in enumerate(line):
                curt = False
                if (row, column) == current_pos:
                    text = self.font.render(char + self.cursor, True, 'white')
                    curt = True
                else:
                    text = self.font.render(char, True, 'white')
                    
                try:
                    if self.user_passage[row][column] == self.passage[row][column]:
                        self.surf.blit(text, positions[row][column])
                    elif curt:
                        cursor = self.font.render(self.cursor, True, 'white')
                        pos = (positions[row][column][0] + self.FONT_WIDTH, positions[row][column][1])
                        self.surf.blit(cursor, pos)
                except IndexError:
                    print(211)
                    print(row, column)

                    with open('dump.txt', 'w') as f:
                        f.write("\n".join(self.user_passage))
                    
                    with open('dump2.txt', 'w') as f:
                        f.write("\n".join(self.passage))
                    exit()



        self.surf_rect = self.surf.get_rect(center=screen_center)
        self.screen.blit(self.surf, self.surf_rect)
        # # Shadow text
        # for index, line in enumerate(self.passage):
        #     text = self.font.render(line, True, 'white')
        #     text.set_alpha(150)
        #     text_rect = text.get_rect(center=self.screen.get_rect().center)
        #     pos = (text_rect.topleft[0], text_rect.topleft[1] + index * text_rect.height)
        
        #     positions.append(pos)

        #     self.screen.blit(text, pos)
            
        # # User text
        # for index, line in enumerate(self.user_passage):
        #     if index == self.current_line:
        #         line += self.cursor
            
        #     compliment = len(self.passage[index]) - len(self.user_passage[index])
        #     buffer = " "*compliment
        #     line += buffer
        #     text = self.font.render(line, True, 'white')

        #     self.screen.blit(text, positions[index])
    


