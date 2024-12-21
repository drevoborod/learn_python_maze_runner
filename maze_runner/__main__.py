import time

import pygame

from maze_runner.draw import GameBoard, Messages, update_display
from maze_runner.game_objects import Wall
from maze_runner.engine import Engine, get_player_direction
from maze_runner.gamefield import FixedMaze


def should_run() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def run_game():
    pygame.init()

    player_speed = 5
    enemy_speed = 2
    maze = FixedMaze(Wall.width, Wall.height)
    engine = Engine(maze, enemies_count=5)
    screen = pygame.display.set_mode((Wall.width * engine.maze_width, Wall.height * engine.maze_height))
    board = GameBoard(engine.context, screen)
    board.draw_static()

    timer_begin = time.time()

    run = True
    lost = False
    clock = pygame.time.Clock()

    while run:
        run = should_run()

        board.draw_dynamic()
        update_display()
        engine.move_all_enemies(enemy_speed)

        new_direction = get_player_direction()
        engine.move_actor(engine.context.player, player_speed, new_direction)

        if engine.player_meets_enemy():
            run = False
            lost = True

        engine.player_finds_bonus()
        clock.tick(60) / 1000

    if lost:
        run = True
        messages = Messages(screen)
        game_over_message = messages.gameover_message()
        timer_message = messages.timer_message(
            timer_begin,
            vertical_offset=game_over_message.get_height()
        )
        messages.scores_message(
            engine.context.score,
            vertical_offset=game_over_message.get_height() + timer_message.get_height()
        )
        update_display()

        while run:
            run = should_run()

    pygame.quit()


if __name__ == "__main__":
    run_game()
