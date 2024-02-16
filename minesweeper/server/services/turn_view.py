from typing import Set, List, NamedTuple

from django.shortcuts import get_object_or_404

from server.models import Game, Mine
from server.services.create_fields import _get_coordinates


class Coord(NamedTuple):
    x_width: int
    y_height: int


def get_game_model(validated_data: dict) -> Game:
    game_id = validated_data.get('game_id')
    game = get_object_or_404(
        Game.objects.prefetch_related('mines'),
        game_id__exact=game_id
    )
    return game


def update_game(game: Game, validated_data: dict) -> Game:
    new_coord = Coord(validated_data.get('col'), validated_data.get('row'))

    coordinates = _get_coordinates(game)
    if new_coord in coordinates:
        game = _game_over(game, coordinates)
    else:
        game = _next_game_turn(game, new_coord)
    game.save()
    return game


def _game_over(game: Game, coordinates: Set[Coord]) -> Game:
    game.completed = True
    game.field = _open_field(game, coordinates)
    return game


def _next_game_turn(game: Game, new_coord: Coord) -> Game:
    field = game.field
    field_mines = game.field_mines

    stack_coordinates = [new_coord]
    visited_coordinates = set()

    while stack_coordinates:
        coord = stack_coordinates.pop()
        if coord in visited_coordinates or not _is_valid_coord(coord, game):
            continue

        visited_coordinates.add(coord)
        cell_field = _add_cell_to_field(field, field_mines, coord)
        if cell_field == 0:
            _add_neighbor_coordinates(stack_coordinates, coord)

    game.field = field
    return game


def _open_field(game: Game, coordinates: Set[Coord], is_win: bool = True) \
        -> List[List[str | int]]:
    if is_win:
        return game.field_mines

    field_mines = game.field_mines
    for coord in coordinates:
        field_mines[coord.x_width][coord.y_height] = 'X'
    return field_mines


def _is_valid_coord(coord: Coord, game: Game) -> bool:
    return 0 <= coord.x_width < game.width and \
    0 <= coord.y_height < game.height


def _add_cell_to_field(
        field: List[List[str | int]],
        field_mines: List[List[str | int]],
        coord: Coord
) -> int:
    cell_field = field_mines[coord.x_width][coord.y_height]
    field[coord.x_width][coord.y_height] = cell_field
    return cell_field


def _add_neighbor_coordinates(stack_coordinates: List[Coord], coord: Coord):
    for x in range(coord.x_width - 0, coord.x_width + 2):
        for y in range(coord.y_height - 0, coord.y_height + 2):
            stack_coordinates.append(Coord(x, y))
