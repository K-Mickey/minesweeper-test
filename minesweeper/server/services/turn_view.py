from typing import Set, List, NamedTuple

from django.shortcuts import get_object_or_404

from server.models import Game
from server.services.create_fields import _get_coordinates
from server.settings import MAX_WIDTH_GRID, MAX_HEIGHT_GRID


class Coord(NamedTuple):
    x_width: int
    y_height: int


def get_game(validated_data: dict) -> Game:
    game_id = validated_data.get('game_id')
    game = get_object_or_404(
        Game.objects.select_related('mines'),
        game_id=game_id
    )
    return game


def update_game(game: Game, validated_data: dict) -> Game:
    new_coord = Coord(validated_data.get('col'), validated_data.get('row'))

    coordinates = _get_coordinates(game)
    if new_coord in coordinates:
        game = game_over(game, coordinates)
    else:
        game = next_turn(game, new_coord)
    game.save()
    return game


def game_over(game: Game, coordinates: Set[Coord]) -> Game:
    game.completed = True
    game.field = show_field(game, coordinates)
    return game


def next_turn(game: Game, new_coord: Coord) -> Game:
    field = game.field
    field_mines = game.field_mines
    cell_field = field_mines[new_coord.x_width][new_coord.y_height]

    field[new_coord.x_width][new_coord.y_height] = cell_field
    for x in range(new_coord.x_width - 1, new_coord.x_width + 2):
        for y in range(new_coord.y_height - 1, new_coord.y_height + 2):
            is_new_coord = x == new_coord.x_width and y == new_coord.y_height
            is_valid_coord = 0 <= x < MAX_WIDTH_GRID and 0 <= y < MAX_HEIGHT_GRID
            if not is_new_coord and is_valid_coord:
                return next_turn(game, Coord(x, y))

    game.field = field
    return game


def show_field(game: Game, coordinates: Set[Coord], is_win: bool = True) -> List[List[str | int]]:
    if is_win:
        return game.field_mines

    field_mines = game.field_mines
    for coord in coordinates:
        field_mines[coord.x_width][coord.y_height] = 'X'
    return field_mines
