from dataclasses import dataclass
import random

import pygame
from pygame.sprite import Group, spritecollide

from maze_runner.game_objects import Player, Enemy1, Background, Wall, Movable, Bonus, Direction
from maze_runner.gamefield import Maze, Point


@dataclass
class Context:
    player: Player
    enemies: Group
    background: Group
    walls: Group
    bonus: Bonus
    score: int


class Engine:
    def __init__(self, maze: Maze, enemies_count: int = 3):
        self.maze = maze
        self.walls_coords, self.background_coords, self.maze_width, self.maze_height = self.maze.generate()
        enemy_positions = random.choices(self.background_coords[1:], k=enemies_count)
        self.context = Context(
            player=Player(*self.background_coords[0]),
            enemies=Group(*[Enemy1(*coords) for coords in enemy_positions]),
            background=Group(*[Background(*coords) for coords in self.background_coords]),
            walls=Group(*[Wall(*coords) for coords in self.walls_coords]),
            bonus=Bonus(*self.new_bonus_position()),
            score=0,
        )

    def new_bonus_position(self) -> Point:
        return random.choice(self.background_coords[1:])

    def move_actor(self, actor: Movable, speed: int, direction: Direction) -> bool:
        old_coordinates = actor.coordinates
        actor.move(direction.value[0] * speed, direction.value[1] * speed)
        if spritecollide(actor, self.context.walls, dokill=False):
            actor.coordinates = old_coordinates
            return False
        return True

    def move_enemy_new_direction(self, enemy: Enemy1, speed: int):
        cannot_move = True
        while cannot_move:
            possible_directions = {Direction.left, Direction.right, Direction.up, Direction.down}
            possible_directions.remove(enemy.current_direction)
            direction = random.choice(list(possible_directions))
            if self.move_actor(enemy, speed, direction):
                cannot_move = False
                enemy.current_direction = direction
                enemy.choose_current_sprite()
                enemy.current_path_length = 1

    def move_all_enemies(self, speed: int):
        for enemy in self.context.enemies:
            if enemy.current_path_length >= random.randint(Background.height * 4, Background.height * 10):
                self.move_enemy_new_direction(enemy, speed)
            else:
                if self.move_actor(enemy, speed, enemy.current_direction):
                    enemy.current_path_length += 1
                else:
                    self.move_enemy_new_direction(enemy, speed)

    def player_meets_enemy(self) -> bool:
        if spritecollide(self.context.player, self.context.enemies, dokill=True):
            return True
        return False

    def player_finds_bonus(self):
        if self.context.bonus.is_collided_with(self.context.player):
            self.context.score += 1
            self.context.bonus.coordinates = self.new_bonus_position()


def get_player_direction() -> Direction:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        return Direction.up
    if keys[pygame.K_DOWN]:
        return Direction.down
    if keys[pygame.K_LEFT]:
        return Direction.left
    if keys[pygame.K_RIGHT]:
        return Direction.right
    return Direction.unknown
