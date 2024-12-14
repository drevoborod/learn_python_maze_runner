import random
import time

import pygame
from pygame.sprite import Group, spritecollide

from maze_runner.game_objects import Wall, Player, Enemy1, Background, Text, Movable
from maze_runner.engine import Context


def maze_coordinates(
        wall_width: int, wall_height: int
) -> tuple[list[tuple[int, int]], list[tuple[int, int]], int, int]:
    matrix = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
    maze_coords = []
    empty_coords = []
    for row_num, row in enumerate(matrix):
        for col_num, col in enumerate(row):
            coords = (col_num * wall_width, row_num * wall_height)
            if col == 1:
                maze_coords.append(coords)
            else:
                empty_coords.append(coords)
    return maze_coords, empty_coords, len(matrix[0]), len(matrix)


def prepare_context() -> tuple[Context, int, int]:
    walls_coords, background_coords, maze_width,maze_height = maze_coordinates(Wall.width, Wall.height)
    enemy_positions = random.choices(background_coords[1:], k=3)
    return Context(
        player=Player(*background_coords[0]),
        enemies=Group(*[Enemy1(*coords) for coords in enemy_positions]),
        background=Group(*[Background(*coords) for coords in background_coords]),
        walls=Group(*[Wall(*coords) for coords in walls_coords]),
    ), maze_width, maze_height


def draw_all(screen, context: Context):
    context.background.draw(screen)
    context.enemies.draw(screen)
    context.player.draw(screen)


def actor_moves(context: Context, actor: Movable, speed: int, direction: tuple[int, int]) -> bool:
    old_coordinates = actor.coordinates
    actor.move(direction[0] * speed, direction[1] * speed)
    if spritecollide(actor, context.walls, dokill=False):
        actor.coordinates = old_coordinates
        return False
    return True


def move_enemy_new_direction(context: Context, enemy: Enemy1, speed: int):
    cannot_move = True
    while cannot_move:
        possible_directions = {(0, 1), (0, -1), (-1, 0), (1, 0)}
        possible_directions.remove(enemy.current_direction)
        direction = random.choice(list(possible_directions))
        if actor_moves(context, enemy, speed, direction):
            cannot_move = False
            enemy.current_direction = direction
            enemy.current_path_length = 1


def move_all_enemies(context: Context, speed: int):
    for enemy in context.enemies:
        if enemy.current_path_length >= random.randint(20, 100):
            move_enemy_new_direction(context, enemy, speed)
        else:
            if actor_moves(context, enemy, speed, enemy.current_direction):
                enemy.current_path_length += 1
            else:
                move_enemy_new_direction(context, enemy, speed)


def should_run() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def play():
    pygame.init()

    clock = pygame.time.Clock()
    player_speed = 5
    enemy_speed = 2
    lost = False
    context, maze_width, maze_height = prepare_context()
    screen = pygame.display.set_mode((Wall.width * maze_width, Wall.height * maze_height))
    context.walls.draw(screen)

    timer_begin = time.time()

    run = True

    while run:
        run = should_run()

        draw_all(screen, context)
        pygame.display.flip()

        move_all_enemies(context, enemy_speed)

        keys = pygame.key.get_pressed()

        new_direction = (0, 0)
        if keys[pygame.K_UP]:
            new_direction = (0, -1)
        if keys[pygame.K_DOWN]:
            new_direction = (0, 1)
        if keys[pygame.K_LEFT]:
            new_direction = (-1, 0)
        if keys[pygame.K_RIGHT]:
            new_direction = (1, 0)

        actor_moves(context, context.player, player_speed, new_direction)

        if spritecollide(context.player, context.enemies, dokill=True):
            run = False
            lost = True

        clock.tick(60) / 1000

    if lost:
        run = True
        gameover = Text(
            "GAME OVER",
            (100, screen.get_height() // 2),
            font_size=100,
            font_color=(255, 0, 0)
        )
        gameover.draw(screen)
        score_message = f"Survived for {time.time() - timer_begin:.2f} seconds"
        score = Text(
            score_message,
            (100, screen.get_height() // 2 + gameover.get_height()),
            font_size=30,
            font_color=(0, 0, 0)
        )
        score_size = score.size(score_message)
        pygame.draw.rect(screen, (255, 255, 255), (98, screen.get_height() // 2 + gameover.get_height() - 2, score_size[0] + 2, score_size[1] + 2))

        score.draw(screen)
        pygame.display.flip()
        while run:
            run = should_run()

    pygame.quit()


if __name__ == "__main__":
    play()