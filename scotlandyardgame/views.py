import json
from re import compile, search

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.cache import patch_response_headers

from scotlandyardgame.engine.map import MAP

from . import multiplayer
from .engine.constants import AVAILABLE_COLORS, GameState

name_re = compile(r"^\w+$")


def redirect_with_error(location, errmsg):
    return redirect(reverse(location, kwargs={"error": errmsg}))


def index(request: HttpRequest, game_id=None, error=None):
    player_id = request.session["player_id"]
    is_joining = game_id is not None
    context = {
        "game_id": game_id if is_joining else "",
        "is_joining": is_joining,
        "player_id": player_id,
        "error": error,
    }

    if not is_joining:
        game_id = multiplayer.get_player_connected_game(player_id)
        if game_id is not None:
            print("player already connected, redirecting")
            return redirect(
                "lobby"
                if multiplayer.get_game_by_id(game_id).state == GameState.PENDING
                else "game"
            )
    elif game_id not in multiplayer.GAMES:
        return redirect_with_error("indexerror", f"no such game with ID {game_id}")

    if request.method == "POST":  # (create and) join game
        player_name = request.POST.get("player_name")
        if not search(name_re, player_name):
            return redirect_with_error("indexerror", "invalid name")

        try:
            if not is_joining:
                game_id = multiplayer.create_room()
            multiplayer.join_room(game_id, player_id, player_name)

        except Exception as e:

            print(f"\033[31merror creating lobby: {e}\033[0m")
            return redirect(
                reverse("indexerror", args=["could not join game: " + str(e)])
            )

        print("\033[32mjoined\033[0m, redirecting to lobby")
        return redirect("lobby")

    return render(request, "scotlandyardgame/index.html", context=context)


def lobby(request: HttpRequest):
    player_id = request.session["player_id"]
    game_id = multiplayer.get_game_id_with_player(player_id)
    if game_id is None:
        return redirect_with_error("indexerror", "not in game")

    if (
        game := multiplayer.get_game_by_id(game_id)
    ).state == multiplayer.GameState.STOPPED:
        return redirect_with_error("indexerror", "game stopped")
    if game.state == multiplayer.GameState.RUNNING:
        return redirect("game")

    context = game.get_player_info(player_id)
    print(f"{context['name']} in lobby")

    res = render(request, "scotlandyardgame/lobby.html")
    patch_response_headers(res, cache_timeout=2)
    return res


def game(request: HttpRequest):
    player_id = request.session["player_id"]
    game_id = multiplayer.get_game_id_with_player(player_id)
    if game_id is None:
        return redirect_with_error("indexerror", "not in game")
    if (
        game := multiplayer.get_game_by_id(game_id)
    ).state == multiplayer.GameState.STOPPED:
        return redirect_with_error("indexerror", "game stopped")
    if game.state == multiplayer.GameState.PENDING:
        return redirect("lobby")

    context = game.get_player_info(player_id) | {
        "board": MAP.generate_board_rectangular((15, 20)).tolist(),
        "coords": MAP.coordinates,
        "map_data": MAP.map_data,
        "limits": {
            "max": MAP.limits["max"].tolist(),
            "min": MAP.limits["min"].tolist(),
        },
    }
    print(f"{context['name']} in game")
    return render(request, "scotlandyardgame/game.html", context=context)


def info(request: HttpRequest):
    player_id = request.session["player_id"]
    game_id = multiplayer.get_game_id_with_player(player_id)
    if game_id is None:
        player_info = {"player_id": player_id}
    else:
        player_info = multiplayer.get_game_by_id(game_id).get_player_info(player_id)
    return HttpResponse(json.dumps(player_info), content_type="application/json")


def map(request: HttpRequest):
    return HttpResponse(json.dumps({"map_data": MAP.map_data, "coordinates": MAP.coordinates}), content_type="application/json")