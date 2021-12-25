import pygame
from typing import List, Tuple, Union

Pos = Union[Tuple[int, int], List[int], pygame.Vector2]
Size = Tuple[int, int]
Color = Union[Tuple[int, int, int], List[int], pygame.Color]
Events = List[pygame.event.Event]
