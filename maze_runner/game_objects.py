from abc import ABC
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from pygame import Surface
from pygame.sprite import Sprite
from pygame.image import load
from pygame.transform import smoothscale


class Direction(Enum):
    unknown = (0, 0)
    left = (-1, 0)
    right = (1, 0)
    up = (0, -1)
    down = (0, 1)


@dataclass
class SpritePaths:
    left: str
    right: str
    up: str
    down: str


@dataclass
class Sprites:
    left: Surface
    right: Surface
    up: Surface
    down: Surface


class GameObject(Sprite, ABC):
    width: int = 50
    height: int = 50
    image: Surface

    def __init__(self, x: int, y: int):
        super().__init__()
        self.rect = self.image.get_rect()
        self.coordinates = x, y

    def prepare_sprite(self, sprite_path: str) -> Surface:
        return smoothscale(load(Path(__file__).parent / "resources" / sprite_path), (self.width, self.height))

    def draw(self, surface: Surface) -> None:
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def is_collided_with(self, other: 'GameObject') -> bool:
        return self.rect.colliderect(other.rect)

    @property
    def coordinates(self):
        return self.rect.topleft

    @coordinates.setter
    def coordinates(self, coords: tuple[int, int]):
        self.rect.topleft = coords[0], coords[1]


class Static(GameObject, ABC):
    sprite_filename: str

    def __init__(self, x: int, y: int):
        self.image = self.prepare_sprite(self.sprite_filename)
        super().__init__(x, y)


class Movable(GameObject, ABC):
    width = 40
    height = 40
    sprite_filenames: SpritePaths

    def __init__(self, x: int, y: int):
        self.sprites = Sprites(
            left=self.prepare_sprite(self.sprite_filenames.left),
            right=self.prepare_sprite(self.sprite_filenames.right),
            up=self.prepare_sprite(self.sprite_filenames.up),
            down=self.prepare_sprite(self.sprite_filenames.down),
        )
        self.image = self.sprites.right
        super().__init__(x, y)
        self.current_path_length: int = 0
        self.current_direction: Direction = Direction.right

    def move(self, x_distance, y_distance):
        self.rect = self.rect.move(x_distance, y_distance)

    def choose_current_sprite(self):
        if self.current_direction == Direction.left:
            self.image = self.sprites.left
        elif self.current_direction == Direction.right:
            self.image = self.sprites.right
        elif self.current_direction == Direction.up:
            self.image = self.sprites.up
        elif self.current_direction == Direction.down:
            self.image = self.sprites.down


class Player(Movable):
    sprite_filenames = SpritePaths(
        left="player.png",
        right="player.png",
        up="player.png",
        down="player.png",
    )


class Enemy1(Movable):
    sprite_filenames = SpritePaths(
        left="enemy_l.png",
        right="enemy_r.png",
        up="enemy_r.png",
        down="enemy_l.png",
    )

    def __init__(self, x_distance, y_distance):
        super().__init__(x_distance, y_distance)
        self.current_path_length: int = 0


class Wall(Static):
    sprite_filename = "wall.png"


class Background(Static):
    sprite_filename = "background.png"


class Bonus(Static):
    sprite_filename = "bonus.png"
    width = 40
    height = 40
