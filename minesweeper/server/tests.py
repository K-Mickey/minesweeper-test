from collections import Counter
from itertools import chain

from django.test import TestCase

from minesweeper.server.models import Game
from minesweeper.server.serializers import GameSerializer


class GameCreationPositiveTests(TestCase):
    def setUp(self) -> None:
        serializer = GameSerializer(data={
            'width': 10,
            'height': 10,
            'mines_count': 10
        })
        serializer.is_valid()
        serializer.create(serializer.validated_data)

    def test_game_creation(self):
        game = Game.objects.first()
        self.assertEqual(game.width, 10)
        self.assertEqual(game.height, 10)
        self.assertEqual(game.mines_count, 10)
        self.assertEqual(game.field, [[' '] * 10 for _ in range(10)])

    def test_field_mines(self):
        game = Game.objects.first()
        field_mines = game.field_mines
        mines_counter = Counter(chain.from_iterable(field_mines))

        for cell, count in mines_counter.items():
            if cell == 'M':
                self.assertEqual(count, 10)
            else:
                # Так как рядом с ячейкой не может быть больше 8 мин
                self.assertLess(cell, 9)

    def test_mines(self):
        game = Game.objects.first()
        mines = game.mines
        self.assertEqual(mines.count(), 10)

        unique_mines = set()
        for mine in mines:
            self.assertLess(mine.x_width, 10)
            self.assertLess(mine.y_height, 10)
            self.assertGreaterEqual(mine.x_width, 0)
            self.assertGreaterEqual(mine.y_height, 0)

            unique_mines.add((mine.x_width, mine.y_height))

        self.assertEqual(len(unique_mines), 10)


class GameCreationNegativeTests():
    def test_mines_count_too_big(self):
        serializer = GameSerializer(data={
            'width': 10,
            'height': 10,
            'mines_count': 100
        })
        serializer.is_valid()
        with self.assertRaises(ValueError):
            serializer.create(serializer.validated_data)

    def test_mines_count_too_small(self):
        serializer = GameSerializer(data={
            'width': 10,
            'height': 10,
            'mines_count': 0
        })
        serializer.is_valid()
        with self.assertRaises(ValueError):
            serializer.create(serializer.validated_data)
