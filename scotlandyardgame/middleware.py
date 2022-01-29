from django.http import HttpRequest
from uuid import uuid4


class PlayerIdMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if "player_id" not in request.session:
            request.session["player_id"] = str(uuid4())

        response = self.get_response(request)
        return response
