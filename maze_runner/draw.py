import time

import pygame
from pygame import Surface

from maze_runner.engine import Context
from maze_runner.text import Text


class GameBoard:
    def __init__(self, context: Context, screen: Surface):
        self.context = context
        self.screen = screen

    def draw_dynamic(self):
        self.context.background.draw(self.screen)
        self.context.enemies.draw(self.screen)
        self.context.player.draw(self.screen)
        self.context.bonus.draw(self.screen)

    def draw_static(self):
        self.context.walls.draw(self.screen)


class Messages:
    def __init__(self, screen: Surface):
        self.screen = screen

    def gameover_message(self) -> Text:
        text = Text(
            "GAME OVER",
            (100, self.screen.get_height() // 2),
            font_size=100,
            font_color=(255, 0, 0)
        )
        text.draw(self.screen)
        return text

    def timer_message(self, timer_start: float, vertical_offset: int) -> Text:
        message = f"Survived for {time.time() - timer_start:.2f} seconds"
        text = Text(
            message,
            (100, self.screen.get_height() // 2 + vertical_offset),
            font_size=30,
            font_color=(0, 0, 0)
        )
        text_size = text.size(message)
        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            (98, self.screen.get_height() // 2 + vertical_offset - 2, text_size[0] + 2, text_size[1] + 2)
        )
        text.draw(self.screen)
        return text

    def scores_message(self, score: int, vertical_offset) -> Text:
        message = f"Bonuses found: {score}"
        text = Text(
            message,
            (100, self.screen.get_height() // 2 + vertical_offset),
            font_size=30,
            font_color=(0, 0, 0)
        )
        text_size = text.size(message)
        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            (98, self.screen.get_height() // 2 + vertical_offset - 2, text_size[0] + 2, text_size[1] + 2)
        )
        text.draw(self.screen)
        return text


def update_display():
    pygame.display.flip()
