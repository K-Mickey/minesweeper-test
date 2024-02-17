from rest_framework.exceptions import APIException


class GameCompletedException(APIException):
    status_code = 400
    default_detail = 'Игра уже завершена'
    default_code = 'game_completed'


class AlreadyOpenedException(APIException):
    status_code = 400
    default_detail = 'Ячейка уже открыта'
    default_code = 'already_opened'
