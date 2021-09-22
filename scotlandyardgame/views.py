from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse

from . import multiplayer


def index(request: HttpRequest, game_id='', error=None):
    player_id = request.session["player_id"]
    context = {
        'game_id': game_id,
        'isJoining': "true" if game_id != '' else "false",
        'player_id': player_id,
        'error': error,
        'action': '/lobby' if game_id != '' else '/'
    }
    print(context)

    if request.method == "POST":  # (create and) join game
        player_name = request.POST.get("player_name")
        if not player_name:
            return redirect(reverse("index"), args=["empty name"])

        try:
            game_id = multiplayer.createRoom()
            multiplayer.joinRoom(game_id, player_id, player_name)
        except Exception as e:
            print(f"\033[31merror creating lobby: {context}\033[0m")

            return redirect(reverse("indexerror", args=["could not join game: " + str(e)]))

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
