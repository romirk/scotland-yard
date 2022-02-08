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
        "game_id": game_id if is_joining else ""    ,
        "is_joining": is_joining,
        "player_id": player_id,
        "error": error,
    }

    if not is_joining:
        game_id = multiplayer.getPlayerConnectedGame(player_id)
        if game_id is not None:
            print("player already connected, redirecting")
            return redirect(
                "lobby"
                if multiplayer.getGameByID(game_id).state == GameState.PENDING
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
                game_id = multiplayer.createRoom()
            multiplayer.joinRoom(game_id, player_id, player_name)

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
    game_id = multiplayer.getGameIDWithPlayer(player_id)
    if game_id is None:
        return redirect_with_error("indexerror", "not in game")

    if (
        game := multiplayer.getGameByID(game_id)
    ).state == multiplayer.GameState.STOPPED:
        return redirect_with_error("indexerror", "game stopped")
    if game.state == multiplayer.GameState.RUNNING:
        return redirect("game")

    context = game.getPlayerInfo(player_id)
    context["colors"] = AVAILABLE_COLORS
    print(f"{context['name']} in lobby")

    res = render(request, "scotlandyardgame/lobby.html", context=context)
    patch_response_headers(res, cache_timeout=2)
    return res


def game(request: HttpRequest):
    player_id = request.session["player_id"]
    game_id = multiplayer.getGameIDWithPlayer(player_id)
    if game_id is None:
        return redirect_with_error("indexerror", "not in game")
    if (
        game := multiplayer.getGameByID(game_id)
    ).state == multiplayer.GameState.STOPPED:
        return redirect_with_error("indexerror", "game stopped")
    if game.state == multiplayer.GameState.PENDING:
        return redirect("lobby")

    context = game.getPlayerInfo(player_id) | {
        "board": MAP.generate_board_rectangular((15, 20)).tolist(),
        "coords": MAP.to_list(),
        "map_data": MAP.map_data,
        "limits": {
            "max": MAP.limits["max"].tolist(),
            "min": MAP.limits["min"].tolist(),
        },
    }
    print(f"{context['name']} in game")
    return render(request, "scotlandyardgame/game.html", context=context)


def dot(request: HttpRequest):
    dot = MAP.to_dot()
    return HttpResponse(dot, content_type="text/plain")
