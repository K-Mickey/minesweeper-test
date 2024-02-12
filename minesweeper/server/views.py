from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Game
from .serializers import GameSerializer


@api_view(['POST'])
def new(request):
    serializer = GameSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.create(serializer.validated_data)
    return Response(serializer.initial_data)


