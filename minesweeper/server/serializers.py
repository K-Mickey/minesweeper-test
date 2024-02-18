from django.core.validators import MinValueValidator
from django.db import transaction
from rest_framework import serializers

from .models import Game
from .services.create_fields import create_field, create_mines, create_field_mines


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            'game_id',
            'width',
            'height',
            'mines_count',
            'completed',
            'field',
        ]

    def create(self, validated_data: dict) -> Game:
        with transaction.atomic():
            game = Game.objects.create(**validated_data)
            game.field = create_field(validated_data)
            create_mines(game, validated_data)
            create_field_mines(game, validated_data)
            return game


class TurnViewSerializer(serializers.Serializer):
    game_id = serializers.CharField()
    col = serializers.IntegerField(
        validators=[
            MinValueValidator(0),
        ]
    )
    row = serializers.IntegerField(
        validators=[
            MinValueValidator(0),
        ]
    )
