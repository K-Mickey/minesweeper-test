from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers

from .models import Game
from .services.create_fields import create_field, create_mines, create_field_mines
from .settings import MIN_WIDTH_GRID, MAX_WIDTH_GRID, MIN_HEIGHT_GRID, MAX_HEIGHT_GRID


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

    def create(self, validated_data: dict) -> Game:
        game = Game.objects.create(**validated_data)
        game.field = create_field(validated_data)
        create_mines(game, validated_data)
        create_field_mines(game)
        return game


class TurnViewSerializer(serializers.Serializer):
    game_id = serializers.CharField()
    col = serializers.IntegerField(
        validators=[
            MinValueValidator(MIN_WIDTH_GRID),
            MaxValueValidator(MAX_WIDTH_GRID),
        ]
    )
    row = serializers.IntegerField(
        validators=[
            MinValueValidator(MIN_HEIGHT_GRID),
            MaxValueValidator(MAX_HEIGHT_GRID),
        ]
    )