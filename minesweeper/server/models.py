import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError

from .settings import MIN_WIDTH_GRID, MAX_WIDTH_GRID, MIN_HEIGHT_GRID, \
    MAX_HEIGHT_GRID, MIN_N_MINES


class Game(models.Model):
    game_id = models.UUIDField(
        verbose_name='Идентификатор игры',
        primary_key=True,
        default=uuid.uuid4,
    )
    width = models.PositiveIntegerField(
        verbose_name='Ширина',
        validators=[
            MinValueValidator(MIN_WIDTH_GRID),
            MaxValueValidator(MAX_WIDTH_GRID),
        ],
    )
    height = models.PositiveIntegerField(
        verbose_name="Высота",
        validators=[
            MinValueValidator(MIN_HEIGHT_GRID),
            MaxValueValidator(MAX_HEIGHT_GRID),
        ],
    )
    mines_count = models.PositiveIntegerField(
        verbose_name='Количество мин',
        validators=[
            MinValueValidator(MIN_N_MINES),
        ],
    )
    completed = models.BooleanField(
        verbose_name='Завершена ли игра',
        default=False,
    )
    field = models.JSONField(
        verbose_name='Поле для игры',
        default=list,
    )
    field_mines = models.JSONField(
        verbose_name='Поле с минами',
        null=True,
    )

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'

    def __str__(self):
        return f'Игра {self.game_id} - ' \
               f'{"завершена" if self.completed else "не завершена"}'

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)

        if self.mines_count >= self.width * self.height:
            raise ValidationError(
                'Количество мин должно быть меньше, чем количество ячеек поля'
            )


class Mine(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='mines',
    )
    x_width = models.PositiveIntegerField()
    y_height = models.PositiveIntegerField()
