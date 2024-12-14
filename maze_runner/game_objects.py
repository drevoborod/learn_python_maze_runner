from pathlib import Path

from pygame import Surface
from pygame.sprite import Sprite
from pygame.image import load
from pygame.transform import smoothscale
from pygame.font import Font


class GameObject(Sprite):
    file_path: str = None
    width = 50
    height = 50

    def __init__(self, x: int, y: int):
        super().__init__()
        self.image = smoothscale(load(Path(__file__).parent / "resources" / self.file_path), (self.width, self.height))
        # self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y

    def draw(self, surface: Surface) -> None:
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def is_collided_with(self, other: 'GameObject') -> bool:
        return self.rect.colliderect(other.rect)


class Movable(GameObject):
    width = 40
    height = 40

    def move(self, x_distance, y_distance):
        self.rect = self.rect.move(x_distance, y_distance)

    @property
    def coordinates(self):
        return self.rect.topleft

    @coordinates.setter
    def coordinates(self, coords: tuple[int, int]):
        self.rect.topleft = coords[0], coords[1]


class Player(Movable):
    file_path = "player.png"


class Enemy1(Movable):
    file_path = "enemy_r.png"

    def __init__(self, x_distance, y_distance):
        super().__init__(x_distance, y_distance)
        self.current_path_length = 0
        self.current_direction = (1, 0)  # (x, y) -> right


class Wall(GameObject):
    file_path = "wall.png"


class Background(GameObject):
    file_path = "background.png"


class Text(Font):
    def __init__(
        self,
        text: str,
        topleft: tuple[int, int],
        font_size: int = 30,
        font_color: tuple[int, int, int] | None = None,
    ) -> None:
        super().__init__(None, font_size)
        self.__font_color = font_color or (255, 255, 255)
        self.__text = text
        self.__topleft = topleft

    def draw(self, surface: Surface) -> None:
        surface.blit(self.render(self.__text, 0, self.__font_color), self.__topleft)