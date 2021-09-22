from django.http import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse
from django.utils.http import urlencode

from . import multiplayer


def index(request: HttpRequest, game_id='', isJoining="false", error=None):
    player_id = request.session["player_id"]
    context = {
        'game_id': game_id,
        'player_id': player_id,
        'isJoining': isJoining,
        'action': '/' if isJoining == "false" else '/lobby',
        'error': error
    }

    if request.method == "POST":
        player_name = request.POST.get("player_name")
        if not player_name:
            context["error"] = "empty name"
            return redirect(reverse("index"), context)

        try:
            game_id = multiplayer.createRoom()
            multiplayer.joinRoom(game_id, player_id, player_name)
        except Exception as e:
            print(f"\033[31merror creating lobby: {e}\033[0m")
            context["error"] = str(e)
            return redirect(reverse("index"), context)

        print("\033[32mjoined\033[0m, redirecting to lobby")
        return redirect(reverse("lobby"))

    return render(request, 'scotlandyardgame/index.html', context=context)


def lobby(request: HttpRequest):
    player_id = request.session["player_id"]
    game_id = multiplayer.getGameWithPlayer(player_id)
    player = multiplayer.games[game_id].getPlayerByID(player_id)
    context = {
        'game_id': game_id,
        'player_id': player_id,
        'name': player.name,
        'color': player.color,
        'isMrX': "true" if player.is_mr_x else "false"
    }
    print(f"{player.name} in lobby")
    return render(request, 'scotlandyardgame/lobby.html', context=context)
