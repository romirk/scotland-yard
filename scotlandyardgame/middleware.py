from django.http import HttpRequest
from uuid import uuid4


class Middleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if "player_id" not in request.session:
            request.session["player_id"] = str(uuid4())
        print("player id: \033[36m" + request.session["player_id"] + "\033[0m")

        response = self.get_response(request)
        return response