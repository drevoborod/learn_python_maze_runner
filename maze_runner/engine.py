from dataclasses import dataclass

from pygame.sprite import Group

from maze_runner.game_objects import Player, Enemy1, Background, Wall


@dataclass
class Context:
    player: Player
    enemies: [list[Enemy1]]
    background: Group
    walls: Group

