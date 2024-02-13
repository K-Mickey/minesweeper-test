import random
from typing import List, Set, Tuple, NamedTuple

from server.models import Game, Mine
from server.settings import MAX_WIDTH_GRID, MAX_HEIGHT_GRID


class Coord(NamedTuple):
    x_width: int
    y_height: int


def create_field(validated_data: dict, default_cell: str | int = ' ') -> List[List]:
    width = validated_data.get('width')
    height = validated_data.get('height')
    return [[default_cell] * height for _ in range(width)]


def create_mines(game: Game, validated_data: dict) -> None:
    mines_coordinates = _get_mine_coordinates(validated_data)
    for x_width, y_height in mines_coordinates:
        Mine.objects.create(
            game=game,
            x_width=x_width,
            y_height=y_height,
        )


def create_field_mines(game: Game) -> None:
    coordinates = _get_coordinates(game)
    field_mines = create_field(game, 0)
    for coord in coordinates:
        field_mines = _add_around_cnt(coord, coordinates, field_mines)
        field_mines[coord.x_width][coord.y_height] = 'M'

    game.field_mines = field_mines
    game.save()


def _add_around_cnt(coord: Coord, coordinates: Set[Coord], field: List[List[int]]) -> int:
    x_min = max(0, coord.x_width - 1)
    x_max = min(coord.x_width + 2, MAX_WIDTH_GRID - 1)
    y_min = max(0, coord.y_height - 1)
    y_max = min(coord.y_height + 2, MAX_HEIGHT_GRID - 1)

    for x_width in range(x_min, x_max):
        for y_height in range(y_min, y_max):
            if Coord(x_width, y_height) in coordinates:
                continue

            cell = field[x_width][y_height]
            field[x_width][y_height] = cell + 1
    return field


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


def _get_coordinates(game: Game) -> Set[Coord]:
    return {Coord(coord.x_width, coord.y_height) for coord in game.mines}
