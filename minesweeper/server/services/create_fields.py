import random
from typing import List, Set, Tuple

from server.models import Game, Mine


def create_field(validated_data: dict) -> List[List]:
    width = validated_data.get('width')
    height = validated_data.get('height')
    return [' ' * height for _ in range(width)]


def create_mines(game: Game, validated_data: dict) -> None:
    mines_coordinates = _get_mine_coordinates(validated_data)
    for x_width, y_height in mines_coordinates:
        Mine.objects.create(
            game=game,
            x_width=x_width,
            y_height=y_height,
        )


def _get_mine_coordinates(validated_data: dict) -> Set[Tuple[int, int]]:
    width = validated_data.get('width')
    height = validated_data.get('height')
    mines_count = validated_data.get('mines_count')

    mines_coordinates = set()
    while len(mines_coordinates) < mines_count:
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        mines_coordinates.add((x, y))
    return mines_coordinates
