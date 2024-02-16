from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import GameSerializer, TurnViewSerializer
from .services.turn_view import get_game_model, update_game


@api_view(['POST'])
def new(request):
    serializer = GameSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.create(serializer.validated_data)
    return Response(serializer.data)


@api_view(['POST'])
def turn(request):
    serializer = TurnViewSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    game = get_game_model(serializer.validated_data)
    game = update_game(game, serializer.validated_data)

    return Response(GameSerializer(game).data)
