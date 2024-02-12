from rest_framework import serializers

from .models import Game
from .services.create_fields import create_field, create_mines


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

    def create(self, validated_data: dict) -> Game:
        game = Game.objects.create(**validated_data)
        game.field = create_field(validated_data)
        create_mines(game, validated_data)
        return game
